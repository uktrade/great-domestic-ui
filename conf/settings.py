# -*- coding: utf-8 -*-

'''
Django settings for Export Readiness project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
'''

import os

import environ

env = environ.Env()


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', False)

# As the app is running behind a host-based router supplied by Heroku or other
# PaaS, we can open ALLOWED_HOSTS
ALLOWED_HOSTS = ['*']

# https://docs.djangoproject.com/en/dev/ref/settings/#append-slash
APPEND_SLASH = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_extensions',
    'raven.contrib.django.raven_compat',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'formtools',
    'corsheaders',
    'directory_constants',
    'core',
    'article',
    'triage',
    'casestudy',
    'directory_healthcheck',
    'health_check',
    'contact',
    'captcha',
    'export_elements',
    'directory_components',
]

MIDDLEWARE_CLASSES = [
    'directory_components.middleware.MaintenanceModeMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'sso.middleware.SSOUserMiddleware',
    'directory_components.middleware.NoCacheMiddlware',
    'core.middleware.LocaleQuerystringMiddleware',
    'core.middleware.PersistLocaleMiddleware',
    'core.middleware.ForceDefaultLocale',
    'directory_components.middleware.RobotsIndexControlHeaderMiddlware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'directory_components.context_processors.sso_processor',
                'directory_components.context_processors.urls_processor',
                ('directory_components.context_processors.'
                    'header_footer_processor'),
                'core.context_processors.feature_flags',
                'directory_components.context_processors.analytics',
            ],
        },
    },
]

WSGI_APPLICATION = 'conf.wsgi.application'


# # Database
# hard to get rid of this
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-gb'

# https://github.com/django/django/blob/master/django/conf/locale/__init__.py
LANGUAGES = [
    ('en-gb', 'English'),               # English
    ('zh-hans', '简体中文'),             # Simplified Chinese
    ('de', 'Deutsch'),                  # German
    ('ja', '日本語'),                    # Japanese
    ('es', 'Español'),                  # Spanish
    ('pt', 'Português'),                # Portuguese
    ('ar', 'العربيّة'),                 # Arabic
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# Static files served with Whitenoise and AWS Cloudfront
# http://whitenoise.evans.io/en/stable/django.html#instructions-for-amazon-cloudfront
# http://whitenoise.evans.io/en/stable/django.html#restricting-cloudfront-to-static-files
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_HOST = env.str('STATIC_HOST', '')
STATIC_URL = STATIC_HOST + '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Logging for development
if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': True,
            },
            'mohawk': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
            'requests': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
        }
    }
else:
    # Sentry logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry'],
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s '
                          '%(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'sentry': {
                'level': 'ERROR',
                'class': (
                    'raven.contrib.django.raven_compat.handlers.SentryHandler'
                ),
                'tags': {'custom-tag': 'x'},
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'raven': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
            'sentry.errors': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
        },
    }


# directory-api
API_CLIENT_BASE_URL = env.str('API_CLIENT_BASE_URL')
API_SIGNATURE_SECRET = env.str('API_SIGNATURE_SECRET')

# directory-sso-proxy
SSO_PROXY_API_CLIENT_BASE_URL = env.str('SSO_PROXY_API_CLIENT_BASE_URL')
SSO_PROXY_SIGNATURE_SECRET = env.str('SSO_PROXY_SIGNATURE_SECRET')
SSO_PROXY_LOGIN_URL = env.str('SSO_PROXY_LOGIN_URL')
SSO_PROXY_LOGOUT_URL = env.str('SSO_PROXY_LOGOUT_URL')
SSO_PROXY_SIGNUP_URL = env.str('SSO_PROXY_SIGNUP_URL')
SSO_PROFILE_URL = env.str('SSO_PROFILE_URL')
SSO_PROXY_REDIRECT_FIELD_NAME = env.str('SSO_PROXY_REDIRECT_FIELD_NAME')
SSO_PROXY_SESSION_COOKIE = env.str('SSO_PROXY_SESSION_COOKIE')

SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', True)
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', 16070400)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# HEADER/FOOTER URLS
HEADER_FOOTER_URLS_GREAT_HOME = env.str('HEADER_FOOTER_URLS_GREAT_HOME', '')
HEADER_FOOTER_URLS_FAB = env.str('HEADER_FOOTER_URLS_FAB', '')
HEADER_FOOTER_URLS_SOO = env.str('HEADER_FOOTER_URLS_SOO', '')
HEADER_FOOTER_URLS_EVENTS = env.str('HEADER_FOOTER_URLS_EVENTS', '')
HEADER_FOOTER_URLS_CONTACT_US = env.str('HEADER_FOOTER_URLS_CONTACT_US', '')
HEADER_FOOTER_URLS_DIT = env.str('HEADER_FOOTER_URLS_DIT', '')
COMPONENTS_URLS_FAS = env.str('COMPONENTS_URLS_FAS', '')

# Exopps url for interstitial page
SERVICES_EXOPPS_ACTUAL = env.str('SERVICES_EXOPPS_ACTUAL', '')

# Sentry
RAVEN_CONFIG = {
    'dsn': env.str('SENTRY_DSN', ''),
}

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', True)
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True

API_CLIENT_CLASSES = {
    'default': 'directory_api_client.client.DirectoryAPIClient',
    'unit-test': 'directory_api_client.dummy_client.DummyDirectoryAPIClient',
}
API_CLIENT_CLASS_NAME = env.str('API_CLIENT_CLASS_NAME', 'default')
API_CLIENT_CLASS = API_CLIENT_CLASSES[API_CLIENT_CLASS_NAME]

# Companies House
COMPANIES_HOUSE_API_KEY = env.str('COMPANIES_HOUSE_API_KEY')
COMPANIES_HOUSE_CLIENT_ID = env.str('COMPANIES_HOUSE_CLIENT_ID', '')
COMPANIES_HOUSE_CLIENT_SECRET = env.str('COMPANIES_HOUSE_CLIENT_SECRET', '')

# Google tag manager
GOOGLE_TAG_MANAGER_ID = env.str('GOOGLE_TAG_MANAGER_ID')
GOOGLE_TAG_MANAGER_ENV = env.str('GOOGLE_TAG_MANAGER_ENV', '')
UTM_COOKIE_DOMAIN = env.str('UTM_COOKIE_DOMAIN')

HEADER_FOOTER_CONTACT_US_URL = env.str('HEADER_FOOTER_CONTACT_US_URL', '')

# CORS
CORS_ORIGIN_ALLOW_ALL = env.str('CORS_ORIGIN_ALLOW_ALL', False)
CORS_ORIGIN_WHITELIST = env.list('CORS_ORIGIN_WHITELIST', default=[])

EXTERNAL_SERVICE_FEEDBACK_URL = env.str(
    'EXTERNAL_SERVICE_FEEDBACK_URL',
    'https://contact-us.export.great.gov.uk/directory/FeedbackForm',
)

# security
X_FRAME_OPTIONS = 'DENY'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Healthcheck
HEALTH_CHECK_TOKEN = env.str('HEALTH_CHECK_TOKEN')

# Comtrade API
COMTRADE_API_TOKEN = env.str('COMTRADE_API_TOKEN', '')

# Google captcha
RECAPTCHA_PUBLIC_KEY = env.str('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = env.str('RECAPTCHA_PRIVATE_KEY')
# NOCAPTCHA = True turns on version 2 of recaptcha
NOCAPTCHA = env.bool('NOCAPTCHA', True)

# Zendesk
CONTACT_ZENDESK_URL = env.str('CONTACT_ZENDESK_URL')
CONTACT_ZENDESK_TOKEN = env.str('CONTACT_ZENDESK_TOKEN')
CONTACT_ZENDESK_USER = env.str('CONTACT_ZENDESK_USER')

LANDING_PAGE_VIDEO_URL = env.str(
    'LANDING_PAGE_VIDEO_URL',
    (
        'https://s3-eu-west-1.amazonaws.com/public-directory-api/'
        'promo-video_web.mp4'
    )
)

# directory CMS
CMS_URL = env.str('CMS_URL')
CMS_SIGNATURE_SECRET = env.str('CMS_SIGNATURE_SECRET')

# Internal CH
INTERNAL_CH_BASE_URL = env.str('INTERNAL_CH_BASE_URL', '')
INTERNAL_CH_API_KEY = env.str('INTERNAL_CH_API_KEY', '')

# geo location
GEOIP_PATH = os.path.join(BASE_DIR, 'core/geolocation_data')
GEOIP_COUNTRY = 'GeoLite2-Country.mmdb'

GEOLOCATION_MAXMIND_DATABASE_FILE_URL = env.str(
    'GEOLOCATION_MAXMIND_DATABASE_FILE_URL',
    (
        'http://geolite.maxmind.com/download/geoip/database/'
        'GeoLite2-Country.tar.gz'
    )
)

# feature flags
FEATURE_FLAGS = {
    'INTERNAL_CH_ON': env.bool('FEATURE_USE_INTERNAL_CH_ENABLED', False),
    'CONTACT_US_ON': env.bool('FEATURE_CONTACT_US_ENABLED', False),
    'PERFORMANCE_DASHBOARD_ON': env.bool(
        'FEATURE_PERFORMANCE_DASHBOARD_ENABLED', False
    ),
    # used by directory-components
    'SEARCH_ENGINE_INDEXING_OFF': env.bool(
        'FEATURE_SEARCH_ENGINE_INDEXING_DISABLED', False
    ),
    # used by directory-components
    'MAINTENANCE_MODE_ON': env.bool('FEATURE_MAINTENANCE_MODE_ENABLED', False),
}
