"""
Django settings for wonderment project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# set the mode for this instance
valid_modes = {'dev', 'prod'}
MODE = str(os.environ.get('WM_MODE', 'dev'))
if MODE not in valid_modes:
    raise ValueError("WM_MODE must be one of %s" % valid_modes)

# utility for getting settings from the environment
NOT_PROVIDED = object()


def env(key, coerce=str, default=NOT_PROVIDED):
    try:
        default = default.get(MODE, NOT_PROVIDED)
    except AttributeError:
        pass

    if default is NOT_PROVIDED:
        val = os.environ.get(key)
        if val is None:
            raise ValueError("Environment variable %s is required." % key)
    else:
        val = os.environ.get(key, default)
    return coerce(val) if val is not None else val


from urllib.parse import urlparse


# utility for parsing a database url
def parse_database_url(url):
    url_parts = urlparse(url)
    return {
        'NAME': url_parts.path[1:],
        'USER': url_parts.username,
        'PASSWORD': url_parts.password,
        'HOST': url_parts.hostname,
        'PORT': url_parts.port,
        'ENGINE': {
            'postgres': 'django.db.backends.postgresql_psycopg2',
            'mysql': 'django.db.backends.mysql',
            'sqlite': 'django.db.backends.sqlite3',
        }[url_parts.scheme],
    }

# Deployment config

SECRET_KEY = env('WM_SECRET_KEY', default={'dev': 'development-secret-key'})
DEBUG = env('WM_DEBUG', bool, default={'dev': True, 'prod': False})
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = env(
    'WM_ALLOWED_HOSTS',
    lambda s: [b.strip() for b in s.split(',')],
    default={'dev': '*'},
)

BASE_URL = env('WM_BASE_URL', default={'dev': 'http://wonderment.hexxie.com:8000'})

DATABASES = {
    'default': env(
        'DATABASE_URL',
        parse_database_url,
        default={
            'dev': 'postgres:///wonderment',
        },
    )
}


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djangosecure',
    'floppyforms',
    'bootstrap3',
    'wonderment',
    'wonderment.spring2015survey',
    'wonderment.fall2015eval',
    'wonderment.spring2016eval',
]

MIDDLEWARE_CLASSES = (
    'djangosecure.middleware.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'wonderment.urls'

WSGI_APPLICATION = 'wonderment.wsgi.application'

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Mountain'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = env('WM_STATIC_URL', default='/static/')
STATIC_ROOT = env(
    'WM_STATIC_ROOT', default=os.path.join(BASE_DIR, 'collected-assets'))
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

LOGIN_URL = '/admin/login/'

SECURE_FRAME_DENY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

USE_SSL = env('WM_USE_SSL', bool, default={'dev': False, 'prod': True})

SESSION_COOKIE_SECURE = USE_SSL
SECURE_SSL_REDIRECT = USE_SSL
if USE_SSL:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Email

EMAIL_BACKEND = {
    'prod': 'django.core.mail.backends.smtp.EmailBackend',
    'dev': 'django.core.mail.backends.console.EmailBackend',
}[MODE]

if MODE == 'prod':
    EMAIL_HOST = env('MAILGUN_SMTP_SERVER')
    EMAIL_PORT = env('MAILGUN_SMTP_PORT')
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = env('MAILGUN_SMTP_LOGIN')
    EMAIL_HOST_PASSWORD = env('MAILGUN_SMTP_PASSWORD')

DEFAULT_FROM_EMAIL = env(
    'WM_DEFAULT_FROM_EMAIL',
    default={'dev': "Wonderment Registration <noreply@localhost>"},
)

SENTRY_DSN = env('SENTRY_DSN', default=None)
if SENTRY_DSN:
    INSTALLED_APPS += ['raven.contrib.django.raven_compat']
    RAVEN_CONFIG = {
        'dsn': SENTRY_DSN,
    }

ADMINS = ['carl@oddbird.net']
