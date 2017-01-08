import os

import fern

env = fern.Env('WM_MODE')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Deployment config

SECRET_KEY = env(
    'WM_SECRET_KEY', mode_defaults={'dev': 'development-secret-key'})
DEBUG = env.boolean('WM_DEBUG', mode_defaults={'dev': 't', 'prod': 'f'})
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = env.comma_list(
    'WM_ALLOWED_HOSTS', mode_defaults={'dev': '*'})

BASE_URL = env(
    'WM_BASE_URL', mode_defaults={'dev': 'http://wonderment.hexxie.com:8000'})

DATABASES = {
    'default': env(
        'DATABASE_URL',
        coerce=fern.parse_dj_database_url,
        mode_defaults={
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
    'floppyforms',
    'bootstrap3',
    'wonderment',
    'wonderment.spring2015survey',
    'wonderment.fall2015eval',
    'wonderment.spring2016eval',
    'wonderment.fall2016eval',
]

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

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

X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

USE_SSL = env.boolean('WM_USE_SSL', mode_defaults={'dev': 'f', 'prod': 't'})

SESSION_COOKIE_SECURE = USE_SSL
SECURE_SSL_REDIRECT = USE_SSL
if USE_SSL:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Email

EMAIL_BACKEND = {
    'prod': 'django.core.mail.backends.smtp.EmailBackend',
    'dev': 'django.core.mail.backends.console.EmailBackend',
}[env.mode]

if env.mode == 'prod':
    EMAIL_HOST = env('MAILGUN_SMTP_SERVER')
    EMAIL_PORT = env('MAILGUN_SMTP_PORT')
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = env('MAILGUN_SMTP_LOGIN')
    EMAIL_HOST_PASSWORD = env('MAILGUN_SMTP_PASSWORD')

DEFAULT_FROM_EMAIL = env(
    'WM_DEFAULT_FROM_EMAIL',
    mode_defaults={'dev': "Wonderment Registration <noreply@localhost>"},
)

SENTRY_DSN = env('SENTRY_DSN', default=None)
if SENTRY_DSN:
    INSTALLED_APPS += ['raven.contrib.django.raven_compat']
    RAVEN_CONFIG = {
        'dsn': SENTRY_DSN,
    }

ADMINS = ['carl@oddbird.net']
