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
ALLOWED_HOSTS = ['http://bct-dev.milosolutions.com/']