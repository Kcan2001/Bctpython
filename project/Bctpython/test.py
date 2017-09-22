from .settings import *  # noqa

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = True
# Mail settings
# ------------------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.googlemail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'admin@blackcrowtours.com'
EMAIL_HOST_PASSWORD = 'Lapoodle123@'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'admin@blackcrowtours.com'
DEFAULT_TO_EMAIL= 'admin@blackcrowtours.com'
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

ADMINS = (
    ("""Michal""", 'msoltysek@milosolutions.com'),
    ("""Igor""", 'idubovik@milosolutions.com'),
)
ALLOWED_HOSTS = ['bct-dev.milosolutions.com']

# Instagram API settings
# You can define how many photos from instagram will be shown at INSTAGRAM_SHOW_MEDIA_COUNT. Note: only 1-20 photos.
INSTAGRAM_ACCESS_TOKEN = '2604665802.a200e72.9da5a0eac5e645e89a2245e555921b40'
INSTAGRAM_CLIENT_ID = 'a200e726a2be40beb58239cf02c08a63'
INSTAGRAM_CLIENT_SECRET = '64b5b44566b74ec49bdcbc450bc80f4e'
INSTAGRAM_SHOW_MEDIA_COUNT = 20

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
POINTS_PER_DOLLAR = 0.2
