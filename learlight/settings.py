"""
Django settings for learlight project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os
import dj_database_url


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

LOGIN_URL = 'login/'
LOGIN_REDIRECT_URL = '/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&1w(v$pkmma^!qo5g@@q64%x4fv9sjym+b@d&5kegtq9h=5kcw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
     'django.contrib.humanize',
    'learlight',
    'dashboard',
    'crm',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'learlight.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'learlight.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
# Parse database configuration from $DATABASE_URL

# DATABASES = {
#     'default': dj_database_url.config(default='postgres://postgres:123456@127.0.0.1:5432/learlight')
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'learlight',                      
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

SYSTEM_ID = 'LLCRM'

# INTERNAL_EMAIL_LIST = os.environ['INTERNAL_EMAIL_LIST'].split(',')
#
# MAILGUN_DOMAIN = os.environ['MAILGUN_DOMAIN']
# MAILGUN_API_URL = os.environ['MAILGUN_API_URL']
# MAILGUN_API_USER = os.environ['MAILGUN_API_USER']
# MAILGUN_API_KEY = os.environ['MAILGUN_API_KEY']


INTERNAL_EMAIL_LIST = ['test2@sandbox87787ac6bd344cae847cd4163e3a20df.mailgun.org',
                       'test@sandbox87787ac6bd344cae847cd4163e3a20df.mailgun.org']

MAILGUN_DOMAIN = 'sandbox87787ac6bd344cae847cd4163e3a20df.mailgun.org'
MAILGUN_API_URL = 'https://api.mailgun.net/v3/'
MAILGUN_API_USER = 'postmaster@sandbox87787ac6bd344cae847cd4163e3a20df.mailgun.org'
MAILGUN_API_KEY = 'key-1a7aa873f1744cbd073273dfe7398726'

#AWS_ACCESS_KEY_ID = 'AKIAJAK56A5CYDR47QIQ'
#AWS_SECRET_ACCESS_KEY = '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'
AWS_ACCESS_KEY_ID = 'AKIAJRXPMV2XK4BT5ATA'
AWS_SECRET_ACCESS_KEY = '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'
S3_BUCKET_NAME = 'elasticbeanstalk-us-east-1-491317748654'

COUNTY_LOOKUP_API_URL = "http://data.fcc.gov/api/block/find?format=json&latitude=%s&longitude=%s"

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
