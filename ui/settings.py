# -*- coding: utf-8 -*-

"""
Django settings for ui project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
from directory_constants.constants import urls as default_urls

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv("DEBUG", False))

# As the app is running behind a host-based router supplied by Heroku or other
# PaaS, we can open ALLOWED_HOSTS
ALLOWED_HOSTS = ['*']

# https://docs.djangoproject.com/en/dev/ref/settings/#append-slash
APPEND_SLASH = True


# Application definition

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    'django.contrib.humanize',
    "django_extensions",
    "raven.contrib.django.raven_compat",
    "django.contrib.sessions",
    "django.contrib.sitemaps",
    "formtools",
    "corsheaders",
    "ui",
    "directory_constants",
    "directory_header_footer",
    "core",
    "article",
    "triage",
    "casestudy",
    "directory_healthcheck",
    "health_check",
    "contact",
    "captcha",
]

MIDDLEWARE_CLASSES = [
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'sso.middleware.SSOUserMiddleware',
    'core.middleware.NoCacheMiddlware',
    'ui.middleware.LocaleQuerystringMiddleware',
    'ui.middleware.PersistLocaleMiddleware',
    'ui.middleware.ForceDefaultLocale',
]

ROOT_URLCONF = 'ui.urls'

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
                'directory_header_footer.context_processors.sso_processor',
                'directory_header_footer.context_processors.urls_processor',
                ('directory_header_footer.context_processors.'
                 'header_footer_context_processor'),
                'core.context_processors.feature_flags',
                'core.context_processors.analytics',
                'core.context_processors.external_service_urls',
            ],
        },
    },
]

WSGI_APPLICATION = 'ui.wsgi.application'


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
STATIC_HOST = os.environ.get('STATIC_HOST', '')
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
API_CLIENT_BASE_URL = os.environ["API_CLIENT_BASE_URL"]
API_SIGNATURE_SECRET = os.environ["API_SIGNATURE_SECRET"]

# directory-sso-proxy
SSO_PROXY_API_CLIENT_BASE_URL = os.environ["SSO_PROXY_API_CLIENT_BASE_URL"]
SSO_PROXY_SIGNATURE_SECRET = os.environ["SSO_PROXY_SIGNATURE_SECRET"]
SSO_PROXY_LOGIN_URL = os.environ["SSO_PROXY_LOGIN_URL"]
SSO_PROXY_LOGOUT_URL = os.environ["SSO_PROXY_LOGOUT_URL"]
SSO_PROXY_SIGNUP_URL = os.environ["SSO_PROXY_SIGNUP_URL"]
SSO_PROFILE_URL = os.environ["SSO_PROFILE_URL"]
SSO_PROXY_REDIRECT_FIELD_NAME = os.environ["SSO_PROXY_REDIRECT_FIELD_NAME"]
SSO_PROXY_SESSION_COOKIE = os.environ["SSO_PROXY_SESSION_COOKIE"]

ANALYTICS_ID = os.getenv("ANALYTICS_ID")

SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'true') == 'true'
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '16070400'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# HEADER/FOOTER URLS
GREAT_EXPORT_HOME = os.getenv(
    'GREAT_EXPORT_HOME', default_urls.GREAT_EXPORT_HOME)

# EXPORTING PERSONAS
EXPORTING_NEW = os.getenv(
    'EXPORTING_NEW', default_urls.EXPORTING_NEW)
EXPORTING_REGULAR = os.getenv(
    'EXPORTING_REGULAR', default_urls.EXPORTING_REGULAR)
EXPORTING_OCCASIONAL = os.getenv(
    'EXPORTING_OCCASIONAL', default_urls.EXPORTING_OCCASIONAL)

# GUIDANCE/ARTICLE SECTIONS
GUIDANCE_MARKET_RESEARCH = os.getenv(
    'GUIDANCE_MARKET_RESEARCH', default_urls.GUIDANCE_MARKET_RESEARCH)
GUIDANCE_CUSTOMER_INSIGHT = os.getenv(
    'GUIDANCE_CUSTOMER_INSIGHT', default_urls.GUIDANCE_CUSTOMER_INSIGHT)
GUIDANCE_FINANCE = os.getenv('GUIDANCE_FINANCE', default_urls.GUIDANCE_FINANCE)
GUIDANCE_BUSINESS_PLANNING = os.getenv(
    'GUIDANCE_BUSINESS_PLANNING', default_urls.GUIDANCE_BUSINESS_PLANNING)
GUIDANCE_GETTING_PAID = os.getenv(
    'GUIDANCE_GETTING_PAID', default_urls.GUIDANCE_GETTING_PAID)
GUIDANCE_OPERATIONS_AND_COMPLIANCE = os.getenv(
    'GUIDANCE_OPERATIONS_AND_COMPLIANCE',
    default_urls.GUIDANCE_OPERATIONS_AND_COMPLIANCE)

# SERVICES
SERVICES_EXOPPS = os.getenv('SERVICES_EXOPPS', default_urls.SERVICES_EXOPPS)
SERVICES_EXOPPS_ACTUAL = os.getenv(
    'SERVICES_EXOPPS_ACTUAL', default_urls.SERVICES_EXOPPS)
SERVICES_FAB = os.getenv('SERVICES_FAB', default_urls.SERVICES_FAB)
SERVICES_GET_FINANCE = os.getenv(
    'SERVICES_GET_FINANCE', default_urls.SERVICES_GET_FINANCE)
SERVICES_SOO = os.getenv('SERVICES_SOO', default_urls.SERVICES_SOO)

# FOOTER LINKS
INFO_ABOUT = os.getenv('INFO_ABOUT', default_urls.INFO_ABOUT)
INFO_CONTACT_US_DIRECTORY = os.getenv(
    'INFO_CONTACT_US_DIRECTORY',
    default_urls.INFO_CONTACT_US_DIRECTORY)
INFO_PRIVACY_AND_COOKIES = os.getenv(
    'INFO_PRIVACY_AND_COOKIES',
    default_urls.INFO_PRIVACY_AND_COOKIES)
INFO_TERMS_AND_CONDITIONS = os.getenv(
    'INFO_TERMS_AND_CONDITIONS',
    default_urls.INFO_TERMS_AND_CONDITIONS)

# Sentry
RAVEN_CONFIG = {
    "dsn": os.getenv("SENTRY_DSN"),
}

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'true') == 'true'
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True

API_CLIENT_CLASSES = {
    'default': 'directory_api_client.client.DirectoryAPIClient',
    'unit-test': 'directory_api_client.dummy_client.DummyDirectoryAPIClient',
}
API_CLIENT_CLASS_NAME = os.getenv('API_CLIENT_CLASS_NAME', 'default')
API_CLIENT_CLASS = API_CLIENT_CLASSES[API_CLIENT_CLASS_NAME]

# Companies House
COMPANIES_HOUSE_API_KEY = os.environ['COMPANIES_HOUSE_API_KEY']
COMPANIES_HOUSE_CLIENT_ID = os.getenv('COMPANIES_HOUSE_CLIENT_ID')
COMPANIES_HOUSE_CLIENT_SECRET = os.getenv('COMPANIES_HOUSE_CLIENT_SECRET')

# Google tag manager
GOOGLE_TAG_MANAGER_ID = os.environ['GOOGLE_TAG_MANAGER_ID']
GOOGLE_TAG_MANAGER_ENV = os.getenv('GOOGLE_TAG_MANAGER_ENV', '')
UTM_COOKIE_DOMAIN = os.environ['UTM_COOKIE_DOMAIN']

HEADER_FOOTER_CONTACT_US_URL = os.getenv(
    'HEADER_FOOTER_CONTACT_US_URL',
    default_urls.INFO_CONTACT_US_DIRECTORY,
)

# CORS
CORS_ORIGIN_ALLOW_ALL = os.getenv('CORS_ORIGIN_ALLOW_ALL') == 'true'
CORS_ORIGIN_WHITELIST = os.getenv('CORS_ORIGIN_WHITELIST', '').split(',')

EXTERNAL_SERVICE_FEEDBACK_URL = os.getenv(
    'EXTERNAL_SERVICE_FEEDBACK_URL',
    'https://contact-us.export.great.gov.uk/directory/FeedbackForm',
)

# security
X_FRAME_OPTIONS = 'DENY'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Healthcheck
HEALTH_CHECK_TOKEN = os.environ['HEALTH_CHECK_TOKEN']

# Comtrade API
COMTRADE_API_TOKEN = os.getenv('COMTRADE_API_TOKEN')

# Google captcha
RECAPTCHA_PUBLIC_KEY = os.environ['RECAPTCHA_PUBLIC_KEY']
RECAPTCHA_PRIVATE_KEY = os.environ['RECAPTCHA_PRIVATE_KEY']
# NOCAPTCHA = True turns on version 2 of recaptcha
NOCAPTCHA = os.getenv('NOCAPTCHA') != 'false'

# Zendesk
CONTACT_ZENDESK_URL = os.environ['CONTACT_ZENDESK_URL']
CONTACT_ZENDESK_TOKEN = os.environ['CONTACT_ZENDESK_TOKEN']
CONTACT_ZENDESK_USER = os.environ['CONTACT_ZENDESK_USER']

FEATURE_CONTACT_US_ENABLED = os.getenv(
    'FEATURE_CONTACT_US_ENABLED', 'false'
) == 'true'
