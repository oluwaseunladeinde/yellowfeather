"""
Django settings for yellowfeather project.

Generated by 'django-admin startproject' using Django 1.11.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '<secret_key>'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 2

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',
    'account',
    'urlauth',
    'django_forms_bootstrap',
    'el_pagination',
    'markdown_deux',
    'autofixture',
    'sorl.thumbnail',
    'feather',
    'haystack',
    'auditlog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'account.middleware.LocaleMiddleware',
    'account.middleware.TimezoneMiddleware',
    'account.middleware.ExpiredPasswordMiddleware',

    'core.middleware.RequestParamsMiddleware',
]

AUTHENTICATION_BACKENDS = [

    'account.auth_backends.EmailAuthenticationBackend',
]

ROOT_URLCONF = 'yellowfeather.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'account.context_processors.account',
            ],
        },
    },
]

WSGI_APPLICATION = 'yellowfeather.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

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

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]

MEDIAFILE_DIRS = [
    os.path.join(BASE_DIR, 'media'),
]

FIXTURE_DIRS = [
    os.path.join(BASE_DIR, 'fixtures')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

DAYS_OLD = 7
RECENTLY_ADDED = 3
PROPERTIES_PER_PAGE = 20

#registration
LOGIN_URL = "/'feather/account/login/"
LOGIN_REDIRECT_URL = "/feather/"


ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
SOCIALACCOUNT_QUERY_EMAIL = True


ACCOUNT_ACTIVATION_DAYS = 7
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = False
ACCOUNT_PASSWORD_EXPIRY = 60*60*24*5 # number of seconds, this is 5 days
ACCOUNT_PASSWORD_USE_HISTORY = True
ACCOUNT_SIGNUP_REDIRECT_URL = '/feather/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/feather/'
#ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/feather/account/login/'
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/feather/account/login/'
ACCOUNT_EMAIL_CONFIRMATION_AUTO_LOGIN = True
ACCOUNT_EMAIL_CONFIRMATION_URL = 'feather:account_confirm_email'
ACCOUNT_EMAIL_CONFIRMATION_EMAIL = False


#Haystack config
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 15
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH':    os.path.join(BASE_DIR, 'search_index')
    }
}

PAGINATION_DEFAULT_PAGINATION = 12
ENDLESS_PAGINATION_FIRST_LABEL = '<'
ENDLESS_PAGINATION_LAST_LABEL = '>'
EL_PAGINATION_PER_PAGE = 15

SAVED_SEARCHES_PER_PAGE = 50
SAVED_SEARCHES_THRESHOLD =  1

#Email Server Settings
CONTACT_DEFAULT_EMAIL = '<email>'
DEFAULT_FROM_EMAIL = '<email>'
EMAIL_HOST = '<host>'
EMAIL_HOST_USER = '<email>'
EMAIL_HOST_PASSWORD = '<password>'
EMAIL_PORT = 25
#EMAIL_USE_TLS = True

try:
    from local_settings import *
except ImportError:
    pass
