import os
import urllib
import time
import base64
import hmac

from hashlib import sha1

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.conf import settings


def _landing_view(request):
    view = 'crm:index'
    if request.user.is_superuser:
        view = 'dashboard:index'
    return view


def index(request):
    if request.user.is_authenticated():
        return redirect(reverse(_landing_view(request)))
    return redirect('login')


def user_login(request):
    if not request.user.is_authenticated():
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            else:
                return render(request, 'learlight/login.html', {'error': True})
        else:
            return render(request, 'learlight/login.html', {'error': False})
    return redirect(reverse(_landing_view(request)))


def user_logout(request):
    logout(request)
    return redirect(reverse('login'))


def signed_s3_request(request):
    AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
    # S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
    S3_BUCKET_NAME = settings.S3_BUCKET_NAME

    object_name = urllib.quote_plus(request.GET['file_name'])
    mime_type = request.GET['file_type']

    expires = int(time.time() + 60 * 60 * 24)
    amz_headers = "x-amz-acl:public-read"

    string_to_sign = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires, amz_headers, S3_BUCKET_NAME, object_name)

    signature = base64.encodestring(
        hmac.new(
            AWS_SECRET_ACCESS_KEY.encode(),
            string_to_sign.encode('utf8'),
            sha1
        ).digest()
    )
    signature = urllib.quote_plus(signature.strip())

    url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET_NAME, object_name)

    return JsonResponse({
        'signed_request': '%s?AWSAccessKeyId=%s&Expires=%s&Signature=%s' % (url, AWS_ACCESS_KEY_ID, expires, signature),
        'url': url,
    })
