"""
Django settings for Bctpython project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import raven

RAVEN_CONFIG = {
    'dsn': 'http://da385935ce644993bc71402cf42a45aa:f12c65a8409e40eb8158350f274f193a@sentry.milosolutions.com/64',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    # 'release': raven.fetch_git_sha((os.path.abspath(os.pardir))),
}

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*bf1p1q)c9n&g0a*r(522@f&y26oacz4w%ca8b+yfswmi!#e0y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'blackcrowtours.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'frontpages',
    'accounts',
    'trips',
    'blog',
    'quickbooks',
    'ckeditor',
    'ckeditor_uploader',
    'django_celery_beat',
    'django_celery_results',
    'raven.contrib.django.raven_compat',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Bctpython.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'Bctpython.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases


# [START db_setup]
if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine'):
    # Running on production App Engine, so connect to Google Cloud SQL using
    # the unix socket at /cloudsql/<your-cloudsql-connection string>
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '/cloudsql/black-crow-tours-py:us-central1:blackcrowtours',
            'NAME': 'bctpython',
            'USER': 'kcan2',
            'PASSWORD': 'iloveblackcrowtours',
        }
    }
else:
    # Running locally so connect to either a local MySQL instance or connect to
    # Cloud SQL via the proxy. To start the proxy via command line:
    #
    #     $ cloud_sql_proxy -instances=[INSTANCE_CONNECTION_NAME]=tcp:3306
    #
    # See https://cloud.google.com/sql/docs/mysql-connect-proxy
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
# [END db_setup]

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'static_root')
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static', 'media')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static', 'static_files'),

)

# Determine custom login redirect url (fix bug)
LOGIN_REDIRECT_URL = '/accounts/'

# Backend for email sending to console, only for dev
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Settings for CKEditor
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_RESTRICT_BY_DATE = True

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['Undo', 'Redo'],
            ['TextColor', 'BGColor'],
            ['Maximize', 'ShowBlocks', 'Source'],
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
             'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak'],
        ],
    },
    'blog': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['Undo', 'Redo'],
            ['TextColor', 'BGColor'],
            ['Maximize', 'ShowBlocks', 'Source'],
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
             'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak'],
        ],
        'width': 'auto',
    },
}

# Instagram API settings
# You can define how many photos from instagram will be shown at INSTAGRAM_SHOW_MEDIA_COUNT. Note: only 1-20 photos.
INSTAGRAM_ACCESS_TOKEN = '2604665802.a200e72.9da5a0eac5e645e89a2245e555921b40'
INSTAGRAM_CLIENT_ID = 'a200e726a2be40beb58239cf02c08a63'
INSTAGRAM_CLIENT_SECRET = '64b5b44566b74ec49bdcbc450bc80f4e'
INSTAGRAM_SHOW_MEDIA_COUNT = 20

# Disqus Site URL
DISQUS_EMBED_URL = 'https://bct-1.disqus.com/embed.js'

# Active Campaign API settings
ACTIVECAMPAIGN_URL = 'https://testco51607.api-us1.com'
ACTIVECAMPAIGN_KEY = '92c1ffbfdb174c8688c4c6ac740743d0dd4015d21e9f142d70333a200d039ab59096edf8'

# Stripe API settings
STRIPE_PUBLIC_KEY = 'pk_test_ptZhV15kJSsxmAFr2dAwihNj'
STRIPE_SECRET_KEY = 'sk_test_9mNe1308FFjc2YST0JS22Cd6'
STRIPE_WEBHOOK_SECRET = 'whsec_Vcgs4oARNMP3fp7RJwrhQzHHvulNLBDf'

# User Premium and Points settings
# Premium membership in dollars
# Points: for example: membership 50 * 0.2 = 10 points user will earn
PREMIUM_MEMBERSHIP_PRICE = 50
POINTS_PER_DOLLAR = 1

# OAuth variables
DISCOVERY_DOCUMENT = 'https://developer.api.intuit.com/.well-known/openid_sandbox_configuration/'
CLIENT_ID = 'Q06R45NHwOMcYycjFmG8noSgUkswAyeOglWeqRSIb2LXn5Y6Fe'
CLIENT_SECRET = '5GboyQKO8y7zV4mgDgSt0MTBIH3NSxdXYFPSUVkV'
REDIRECT_URI = 'https://bct-dev.milosolutions.com/quickbooks/auth-code-handler'
ACCOUNTING_SCOPE = 'com.intuit.quickbooks.accounting'
SANDBOX_QBO_BASEURL = 'https://sandbox-quickbooks.api.intuit.com'

# Configuration for Celery
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
