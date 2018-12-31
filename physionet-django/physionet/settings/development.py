import sys

from .base import *

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = 'PhysioNet Automated System <noreply@dev.physionet.org>'
CONTACT_EMAIL = 'PhysioNet Contact <contact@dev.physionet.org>'

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '',
}

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEMO_FILE_ROOT = os.path.join(os.path.abspath(os.path.join(BASE_DIR, os.pardir)), 'demo-files')

MEDIA_ROOT = os.path.join(os.path.abspath(os.path.join(BASE_DIR, os.pardir)), 'media')

if len(sys.argv) > 1 and sys.argv[1] == 'test':
    MEDIA_ROOT = os.path.join(MEDIA_ROOT, 'test')
    STATICFILES_DIRS[0] = os.path.join(STATICFILES_DIRS[0], 'test')
