import ast

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from django.core.exceptions import PermissionDenied

from learlight.models import Account, Customer, Image, LearlightAccountAssociates
from learlight.mailgun import send_mail

from crm.forms import AuthorizationForm, CustomerInfoForm, EmailPhotoForm, QuoteCreateForm, QuoteSummaryForm
# deverma
from django.http import JsonResponse
def _validate_account(request, customer):
    account = Account.objects.get(owner=request.user)
    if account.id != customer.account.id:
        raise PermissionDenied


@login_required()
def index(request):
    #account = Account.objects.get(owner=request.user)
    if request.user.is_superuser:
        account = Account.objects.filter(owner=request.user)
    else:
        #account = Account.objects.filter(owner=request.user)
        account = LearlightAccountAssociates.objects.filter(user = request.user).values('account')
        acoount_list = list(account)
        account = []
        for x in acoount_list:
            print x['account']
            account.append(x['account'])
            print account
        account = Account.objects.filter(pk__in=account)
    return render(request, 'crm/index.html', {
       'account': account
    })


@login_required()
def how_to_proceed(request, associate_id):
    account = Account.objects.get(owner=request.user)
    associate = User.objects.get(id=associate_id)
    customer = Customer(
        account=account,
        associate=associate,
        created_by=associate.id,
        updated_by=associate.id
    )
    customer.save()
    return render(request, 'crm/how_to_proceed.html', {
        'account': account,
        'associate': associate,
        'customer': customer
    })

from json import dumps
from django.core import serializers
@login_required()
def authorization(request, customer_id):
    #return JsonResponse({'foo':'bar'})
    customer = Customer.objects.get(id=customer_id)
    _validate_account(request, customer)
    account = customer.account
    associate = customer.associate
    #foo =serializers.serialize('json', customer)
    #return JsonResponse({'account': request.method})
    if request.method == 'POST':
        form = AuthorizationForm(request.POST)
        if form.is_valid():
            #return JsonResponse({'account': request.method})
            customer.authorized = True
            customer.save()
            return redirect('crm:information', customer.id)
    else:
        if 'quote' in request.GET:
            customer.quote_requested = request.GET.get('quote') is not None
            customer.save()
        form = AuthorizationForm(instance=customer)
    return render(request, 'crm/authorization.html', {
        'account': account,
        'associate': associate,
        'customer': customer,
        'form': form
    })


@login_required()
def information(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    _validate_account(request, customer)
    account = customer.account
    associate = customer.associate
    if request.method == 'POST':
        #form = CustomerInfoForm(request.POST.dict())
        # changed by deverma
        form = CustomerInfoForm(request.POST)
        if form.is_valid():
            customer.first_name = form.cleaned_data['first_name']
            customer.last_name = form.cleaned_data['last_name']
            customer.email = form.cleaned_data['email']
            customer.address = form.cleaned_data['address']
            customer.postal_code = form.cleaned_data['postal_code']
            customer.phone_number = form.cleaned_data['phone_number']
            customer.save(geocode=True)

            if customer.quote_requested:
                return redirect('crm:quote_create', customer.id)
            else:
                return redirect('crm:email_photo', customer.id)
    else:
        form = CustomerInfoForm(instance=customer)

    return render(request, 'crm/information.html', {
        'account': account,
        'associate': associate,
        'customer': customer,
        'form': form
    })


@login_required()
def email_photo(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    _validate_account(request, customer)
    account = customer.account
    associate = customer.associate
    if request.method == 'POST':
        form = EmailPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            jewelry_image_urls = ast.literal_eval(form.cleaned_data['jewelry_image_urls'])
            for url in jewelry_image_urls:
                customer.image_set.create(
                    customer=customer,
                    url=url,
                    category=Image.CATEGORY_JEWELRY,
                    created_by=associate.id,
                    updated_by=associate.id
                )
            return redirect('crm:email_photo_confirmation', customer.id)
    else:
        form = EmailPhotoForm(instance=customer)

    return render(request, 'crm/email_photo.html', {
        'account': account,
        'associate': associate,
        'customer': customer,
        'form': form
    })


@login_required()
def quote_create(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    _validate_account(request, customer)
    account = customer.account
    associate = customer.associate
    if request.method == 'POST':
        form = QuoteCreateForm(request.POST, request.FILES)
        if form.is_valid():
            customer.jewelry_type = form.cleaned_data['jewelry_type']
            customer.jewelry_value = form.cleaned_data['jewelry_value']
            customer.save()
            receipt_image_url = form.cleaned_data['receipt_image_url']
            if receipt_image_url:
                customer.image_set.create(
                    customer=customer,
                    url=receipt_image_url,
                    category=Image.CATEGORY_RECEIPT,
                    created_by=associate.id,
                    updated_by=associate.id
                )
            jewelry_image_urls = form.cleaned_data['jewelry_image_urls']
            if jewelry_image_urls:
                for url in ast.literal_eval(jewelry_image_urls):
                    customer.image_set.create(
                        customer=customer,
                        url=url,
                        category=Image.CATEGORY_JEWELRY,
                        created_by=associate.id,
                        updated_by=associate.id
                    )
            return redirect('crm:quote_summary', customer.id)
    else:
        form = QuoteCreateForm(instance=customer)

    return render(request, 'crm/quote_create.html', {
        'account': account,
        'associate': associate,
        'customer': customer,
        'images': customer.image_set.filter(category=Image.CATEGORY_JEWELRY),
        'form': form
    })


@login_required()
def quote_summary(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    _validate_account(request, customer)
    account = customer.account
    associate = customer.associate
    if request.method == 'POST':
        form = QuoteSummaryForm(request.POST, request.FILES)
        if form.is_valid():
            customer.receipt_image_url = form.cleaned_data['receipt_image_url']
            customer.save()
            return redirect('crm:quote_confirmation', customer.id)
    else:
        form = QuoteSummaryForm(instance=customer)

    return render(request, 'crm/quote_summary.html', {
        'account': account,
        'associate': associate,
        'customer': customer,
        'images': customer.image_set.filter(category=Image.CATEGORY_JEWELRY),
        'form': form
    })


@login_required()
def quote_confirmation(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    _validate_account(request, customer)
    account = customer.account
    associate = customer.associate

    # Send customer email
    subject = "%s - %s, %s || Your Quote from Jewelers Mutual Insurance Company will arrive shortly!" % (
        account.name,
        account.city,
        account.state
    )
    email_template = get_template('crm/email/quote_customer.html')
    content = email_template.render(Context({
        'account': account,
        'associate': associate,
        'customer': customer
    }))
    send_mail(account.email, [customer.email], subject=subject, html=content)

    # Send internal email
    subject = "Quote Request Data || %s" % account.name
    email_template = get_template('crm/email/quote_internal.html')
    content = email_template.render(Context({
        'account': account,
        'associate': associate,
        'customer': customer
    }))
    send_mail(account.email, settings.INTERNAL_EMAIL_LIST, subject=subject, html=content)

    # mark transaction completed
    customer.transaction_completed = True
    customer.save()

    return render(request, 'crm/quote_confirmation.html', {
        'account': account,
        'associate': associate,
        'customer': customer
    })


@login_required()
def email_photo_confirmation(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    _validate_account(request, customer)
    account = customer.account
    associate = customer.associate

    # Send customer email
    subject = "%s - %s, %s || Your LearLite jewelry photo has arrived!" % (
        account.name,
        account.city,
        account.state
    )
    email_template = get_template('crm/email/photo_customer.html')
    content = email_template.render(Context({
        'account': account,
        'associate': associate,
        'customer': customer
    }))
    send_mail(account.email, [customer.email], subject=subject, html=content)

    # mark transaction completed
    customer.transaction_completed = True
    customer.save()

    return render(request, 'crm/email_photo_confirmation.html', {
        'account': account,
        'associate': associate,
        'customer': customer
    })
