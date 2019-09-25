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
from directory_constants import cms
import directory_healthcheck.backends
import healthcheck.backends

env = environ.Env()
for env_file in env.list('ENV_FILES', default=[]):
    env.read_env(f'conf/env/{env_file}')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)

SECRET_KEY = env.str('SECRET_KEY')

DEBUG = env.bool('DEBUG', False)

# As the app is running behind a host-based router supplied by Heroku or other
# PaaS, we can open ALLOWED_HOSTS
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_extensions',
    'raven.contrib.django.raven_compat',
    'django.contrib.contenttypes',  # required by DRF and auth, not using DB
    'django.contrib.sessions',
    'django.contrib.auth',
    'django.contrib.sitemaps',
    'formtools',
    'corsheaders',
    'directory_constants',
    'directory_sso_api_client',
    'core',
    'article',
    'casestudy',
    'finance',
    'directory_healthcheck',
    'captcha',
    'directory_components',
    'euexit',
    'contact',
    'marketaccess',
    'community',
    'marketing',
    'search',
    'ukef',
    'healthcheck',
    'sso',
]

MIDDLEWARE_CLASSES = [
    'directory_components.middleware.MaintenanceModeMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'directory_sso_api_client.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'directory_components.middleware.CheckGATags',
    'directory_components.middleware.NoCacheMiddlware',
    'directory_components.middleware.LocaleQuerystringMiddleware',
    'directory_components.middleware.PersistLocaleMiddleware',
    'directory_components.middleware.ForceDefaultLocale',
    'directory_components.middleware.CountryMiddleware',
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
                (
                    'directory_components.context_processors.'
                    'header_footer_processor'
                ),
                'directory_components.context_processors.feature_flags',
                'directory_components.context_processors.analytics',
                'directory_components.context_processors.cookie_notice',
            ],
        },
    },
]

WSGI_APPLICATION = 'conf.wsgi.application'

VCAP_SERVICES = env.json('VCAP_SERVICES', {})

if 'redis' in VCAP_SERVICES:
    REDIS_URL = VCAP_SERVICES['redis'][0]['credentials']['uri']
else:
    REDIS_URL = env.str('REDIS_URL', '')

if REDIS_URL:
    cache = {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': "django_redis.client.DefaultClient",
        }
    }
else:
    cache = {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }


CACHES = {
    'default': cache,
    'api_fallback': cache,
    'cms_fallback': cache,
}


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/
LANGUAGE_CODE = 'en-gb'

# https://docs.djangoproject.com/en/2.2/ref/settings/#std:setting-LANGUAGE_COOKIE_NAME
LANGUAGE_COOKIE_DEPRECATED_NAME = 'django-language'
# Django's default value for LANGUAGE_COOKIE_DOMAIN is None
LANGUAGE_COOKIE_DOMAIN = env.str('LANGUAGE_COOKIE_DOMAIN', None)

# https://github.com/django/django/blob/master/django/conf/locale/__init__.py
LANGUAGES = [
    ('en-gb', 'English'),               # English
    ('zh-hans', '简体中文'),              # Simplified Chinese
    ('de', 'Deutsch'),                  # German
    ('ja', '日本語'),                    # Japanese
    ('es', 'Español'),                  # Spanish
    ('pt', 'Português'),                # Portuguese
    ('ar', 'العربيّة'),                  # Arabic
    ('fr', 'Français'),                 # French
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

TIME_ZONE = 'UTC'

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# Static files served with Whitenoise and AWS Cloudfront
# http://whitenoise.evans.io/en/stable/django.html#instructions-for-amazon-cloudfront
# http://whitenoise.evans.io/en/stable/django.html#restricting-cloudfront-to-static-files
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_HOST = env.str('STATIC_HOST', '')
STATIC_URL = STATIC_HOST + '/static/'
STATICFILES_STORAGE = env.str(
    'STATICFILES_STORAGE',
    'whitenoise.storage.CompressedManifestStaticFilesStorage'
)

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
DIRECTORY_API_CLIENT_BASE_URL = env.str('API_CLIENT_BASE_URL')
DIRECTORY_API_CLIENT_API_KEY = env.str('API_SIGNATURE_SECRET')
DIRECTORY_API_CLIENT_SENDER_ID = 'directory'
DIRECTORY_API_CLIENT_DEFAULT_TIMEOUT = 15

# directory-sso-proxy
DIRECTORY_SSO_API_CLIENT_BASE_URL = env.str('SSO_API_CLIENT_BASE_URL')
DIRECTORY_SSO_API_CLIENT_API_KEY = env.str('SSO_SIGNATURE_SECRET')
DIRECTORY_SSO_API_CLIENT_SENDER_ID = 'directory'
DIRECTORY_SSO_API_CLIENT_DEFAULT_TIMEOUT = 15
LOGIN_URL = SSO_PROXY_LOGIN_URL = env.str('SSO_PROXY_LOGIN_URL')
SSO_PROXY_LOGOUT_URL = env.str('SSO_PROXY_LOGOUT_URL')
SSO_PROXY_SIGNUP_URL = env.str('SSO_PROXY_SIGNUP_URL')
SSO_PROFILE_URL = env.str('SSO_PROFILE_URL')
SSO_PROXY_REDIRECT_FIELD_NAME = env.str('SSO_PROXY_REDIRECT_FIELD_NAME')
SSO_SESSION_COOKIE = env.str('SSO_SESSION_COOKIE')

SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', True)

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', 16070400)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# HEADER/FOOTER URLS
DIRECTORY_CONSTANTS_URL_GREAT_DOMESTIC = env.str(
    'DIRECTORY_CONSTANTS_URL_GREAT_DOMESTIC', ''
)
DIRECTORY_CONSTANTS_URL_INTERNATIONAL = env.str(
    'DIRECTORY_CONSTANTS_URL_INTERNATIONAL', ''
)
DIRECTORY_CONSTANTS_URL_EXPORT_OPPORTUNITIES = env.str(
    'DIRECTORY_CONSTANTS_URL_EXPORT_OPPORTUNITIES', ''
)
DIRECTORY_CONSTANTS_URL_SELLING_ONLINE_OVERSEAS = env.str(
    'DIRECTORY_CONSTANTS_URL_SELLING_ONLINE_OVERSEAS', ''
)
DIRECTORY_CONSTANTS_URL_EVENTS = env.str(
    'DIRECTORY_CONSTANTS_URL_EVENTS', ''
)
DIRECTORY_CONSTANTS_URL_INVEST = env.str('DIRECTORY_CONSTANTS_URL_INVEST', '')
DIRECTORY_CONSTANTS_URL_FIND_A_SUPPLIER = env.str(
    'DIRECTORY_CONSTANTS_URL_FIND_A_SUPPLIER', ''
)
DIRECTORY_CONSTANTS_URL_SINGLE_SIGN_ON = env.str(
    'DIRECTORY_CONSTANTS_URL_SINGLE_SIGN_ON', ''
)
DIRECTORY_CONSTANTS_URL_FIND_A_BUYER = env.str(
    'DIRECTORY_CONSTANTS_URL_FIND_A_BUYER', ''
)

PRIVACY_COOKIE_DOMAIN = os.getenv('PRIVACY_COOKIE_DOMAIN')

# Exopps url for /export-opportunities redirect
SERVICES_EXOPPS_ACTUAL = env.str('SERVICES_EXOPPS_ACTUAL', '')

# Sentry
RAVEN_CONFIG = {
    'dsn': env.str('SENTRY_DSN', ''),
}

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', True)
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# Companies House
COMPANIES_HOUSE_API_KEY = env.str('COMPANIES_HOUSE_API_KEY')
COMPANIES_HOUSE_CLIENT_ID = env.str('COMPANIES_HOUSE_CLIENT_ID', '')
COMPANIES_HOUSE_CLIENT_SECRET = env.str('COMPANIES_HOUSE_CLIENT_SECRET', '')

# Google tag manager
GOOGLE_TAG_MANAGER_ID = env.str('GOOGLE_TAG_MANAGER_ID')
GOOGLE_TAG_MANAGER_ENV = env.str('GOOGLE_TAG_MANAGER_ENV', '')
UTM_COOKIE_DOMAIN = env.str('UTM_COOKIE_DOMAIN')
GA360_BUSINESS_UNIT = 'GreatDomestic'

# CORS
CORS_ORIGIN_ALLOW_ALL = env.str('CORS_ORIGIN_ALLOW_ALL', False)
CORS_ORIGIN_WHITELIST = env.list('CORS_ORIGIN_WHITELIST', default=[])

# security
X_FRAME_OPTIONS = 'DENY'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Healthcheck
DIRECTORY_HEALTHCHECK_TOKEN = env.str('HEALTH_CHECK_TOKEN')
DIRECTORY_HEALTHCHECK_BACKENDS = [
    directory_healthcheck.backends.APIBackend,
    directory_healthcheck.backends.SingleSignOnBackend,
    directory_healthcheck.backends.FormsAPIBackend
]

# Comtrade API
COMTRADE_API_TOKEN = env.str('COMTRADE_API_TOKEN', '')

# Google captcha
RECAPTCHA_PUBLIC_KEY = env.str('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = env.str('RECAPTCHA_PRIVATE_KEY')
# NOCAPTCHA = True turns on version 2 of recaptcha
NOCAPTCHA = env.bool('NOCAPTCHA', True)

# directory CMS
DIRECTORY_CMS_API_CLIENT_BASE_URL = env.str('CMS_URL')
DIRECTORY_CMS_API_CLIENT_API_KEY = env.str('CMS_SIGNATURE_SECRET')
DIRECTORY_CMS_API_CLIENT_SENDER_ID = 'directory'
DIRECTORY_CMS_API_CLIENT_SERVICE_NAME = cms.EXPORT_READINESS
DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT = 15

# directory clients
DIRECTORY_CLIENT_CORE_CACHE_EXPIRE_SECONDS = env.int(
    'DIRECTORY_CLIENT_CORE_CACHE_EXPIRE_SECONDS',
    60 * 60 * 24 * 30  # 30 days
)

# Internal Companies House search

DIRECTORY_CH_SEARCH_CLIENT_BASE_URL = env.str('INTERNAL_CH_BASE_URL', '')
DIRECTORY_CH_SEARCH_CLIENT_API_KEY = env.str('INTERNAL_CH_API_KEY', '')
DIRECTORY_CH_SEARCH_CLIENT_SENDER_ID = env.str('DIRECTORY_CH_SEARCH_CLIENT_SENDER_ID', 'directory')
DIRECTORY_CH_SEARCH_CLIENT_DEFAULT_TIMEOUT = env.str('DIRECTORY_CH_SEARCH_CLIENT_DEFAULT_TIMEOUT', 5)

# geo location
GEOIP_PATH = os.path.join(BASE_DIR, 'core/geolocation_data')
GEOIP_COUNTRY = 'GeoLite2-Country.mmdb'

GEOLOCATION_MAXMIND_DATABASE_FILE_URL = env.str(
    'GEOLOCATION_MAXMIND_DATABASE_FILE_URL',
    'http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz'
)

# feature flags
FEATURE_FLAGS = {
    'NEW_INTERNATIONAL_HEADER_ON': env.bool('FEATURE_NEW_INTERNATIONAL_HEADER_ENABLED', False),
    'PROTOTYPE_PAGES_ON': env.bool('FEATURE_PROTOTYPE_PAGES_ENABLED', False),
    'NEWS_SECTION_ON': env.bool('FEATURE_NEWS_SECTION_ENABLED', False),
    'INTERNAL_CH_ON': env.bool('FEATURE_USE_INTERNAL_CH_ENABLED', False),
    'EXPORTING_TO_UK_ON': env.bool('FEATURE_EXPORTING_TO_UK_ON_ENABLED', False),
    'MARKET_ACCESS_ON': env.bool('FEATURE_MARKET_ACCESS_ENABLED', False),
    'MARKET_ACCESS_LINK_ON': env.bool('FEATURE_MARKET_ACCESS_GOV_LINK_ENABLED', False),
    'NEW_REGISTRATION_JOURNEY_ON': env.bool('FEATURE_NEW_REGISTRATION_ENABLED', False),
    'MAINTENANCE_MODE_ON': env.bool('FEATURE_MAINTENANCE_MODE_ENABLED', False),  # used by directory-components
    'TEST_SEARCH_API_PAGES_ON': env.bool('FEATURE_TEST_SEARCH_API_PAGES_ENABLED', False),
    'CAPITAL_INVEST_CONTACT_IN_TRIAGE_ON': env.bool('FEATURE_CAPITAL_INVEST_CONTACT_IN_TRIAGE_ENABLED', False),
    'EXPORT_VOUCHERS_ON': env.bool('FEATURE_EXPORT_VOUCHERS_ENABLED', False)
}
if FEATURE_FLAGS['TEST_SEARCH_API_PAGES_ON']:
    DIRECTORY_HEALTHCHECK_BACKENDS.append(healthcheck.backends.SearchSortBackend)

# UK Export Finance
UKEF_PI_TRACKER_JAVASCRIPT_URL = env.str(
    'UKEF_PI_TRACKER_JAVASCRIPT_URL', 'https://pi.pardot.com/pd.js'
)
UKEF_FORM_SUBMIT_TRACKER_URL = env.str('UKEF_FORM_SUBMIT_TRACKER_URL')

# directory forms api client
DIRECTORY_FORMS_API_BASE_URL = env.str('DIRECTORY_FORMS_API_BASE_URL')
DIRECTORY_FORMS_API_API_KEY = env.str('DIRECTORY_FORMS_API_API_KEY')
DIRECTORY_FORMS_API_SENDER_ID = env.str('DIRECTORY_FORMS_API_SENDER_ID')
DIRECTORY_FORMS_API_DEFAULT_TIMEOUT = env.int(
    'DIRECTORY_API_FORMS_DEFAULT_TIMEOUT', 5
)
DIRECTORY_FORMS_API_ZENDESK_SEVICE_NAME = env.str(
    'DIRECTORY_FORMS_API_ZENDESK_SEVICE_NAME', 'directory'
)

# Brexit
EU_EXIT_ZENDESK_SUBDOMAIN = env.str('EU_EXIT_ZENDESK_SUBDOMAIN')
EU_EXIT_INTERNATIONAL_CONTACT_URL = env.str(
    'EU_EXIT_INTERNATIONAL_CONTACT_URL', '/international/eu-exit-news/contact/'
)

# Contact
INVEST_CONTACT_URL = env.str(
    'INVEST_CONTACT_URL', 'https://invest.great.gov.uk/contact/'
)
CAPITAL_INVEST_CONTACT_URL = env.str(
    'CAPITAL_INVEST_CONTACT_URL', 'https://great.gov.uk/international/content/capital-invest/contact/'
)
FIND_A_SUPPLIER_CONTACT_URL = env.str(
    'FIND_A_SUPPLIER_CONTACT_URL',
    'https://trade.great.gov.uk/industries/contact/'
)
CONTACT_DOMESTIC_ZENDESK_SUBJECT = env.str(
    'CONTACT_DOMESTIC_ZENDESK_SUBJECT', 'great.gov.uk contact form'
)
CONTACT_INTERNATIONAL_ZENDESK_SUBJECT = env.str(
    'CONTACT_DOMESTIC_ZENDESK_SUBJECT',
    'great.gov.uk international contact form'
)
CONTACT_SOO_ZENDESK_SUBJECT = env.str(
    'CONTACT_DOMESTIC_ZENDESK_SUBJECT',
    'great.gov.uk Selling Online Overseas contact form'
)
CONTACT_EVENTS_USER_NOTIFY_TEMPLATE_ID = env.str(
    'CONTACT_EVENTS_USER_NOTIFY_TEMPLATE_ID',
    '2d5d556a-e0fa-4a9b-81a0-6ed3fcb2e3da'
)
CONTACT_EVENTS_AGENT_NOTIFY_TEMPLATE_ID = env.str(
    'CONTACT_EVENTS_AGENT_NOTIFY_TEMPLATE_ID',
    'bf11ece5-22e1-4ffd-b2ab-9f0632e6c95b'
)
CONTACT_EVENTS_AGENT_EMAIL_ADDRESS = env.str(
    'CONTACT_EVENTS_AGENT_EMAIL_ADDRESS'
)
CONTACT_DSO_AGENT_NOTIFY_TEMPLATE_ID = env.str(
    'CONTACT_DSO_AGENT_NOTIFY_TEMPLATE_ID',
    'bf11ece5-22e1-4ffd-b2ab-9f0632e6c95b'
)
CONTACT_DSO_AGENT_EMAIL_ADDRESS = env.str(
    'CONTACT_DSO_AGENT_EMAIL_ADDRESS'
)
CONTACT_DSO_USER_NOTIFY_TEMPLATE_ID = env.str(
    'CONTACT_DSO_USER_NOTIFY_TEMPLATE_ID',
    'a6a3db79-944f-4c59-8eeb-2f756019976c'
)
CONTACT_DIT_AGENT_EMAIL_ADDRESS = env.str(
    'CONTACT_DIT_AGENT_EMAIL_ADDRESS'
)
CONTACT_INTERNATIONAL_AGENT_NOTIFY_TEMPLATE_ID = env.str(
    'CONTACT_INTERNATIONAL_AGENT_NOTIFY_TEMPLATE_ID',
    '8bd422e0-3ec4-4b05-9de8-9cf039d258a9'
)
CONTACT_INTERNATIONAL_AGENT_EMAIL_ADDRESS = env.str(
    'CONTACT_INTERNATIONAL_AGENT_EMAIL_ADDRESS'
)
CONTACT_INTERNATIONAL_USER_NOTIFY_TEMPLATE_ID = env.str(
    'CONTACT_INTERNATIONAL_USER_NOTIFY_TEMPLATE_ID',
    'c07d1fb2-dc0c-40ba-a3e0-3113638e69a3'
)
CONTACT_EXPORTING_USER_NOTIFY_TEMPLATE_ID = env.str(
    'CONTACT_EXPORTING_USER_NOTIFY_TEMPLATE_ID',
    '5abd7372-a92d-4351-bccb-b9a38d353e75'
)
CONTACT_EXPORTING_USER_REPLY_TO_EMAIL_ID = env.str(
    'CONTACT_EXPORTING_USER_REPLY_TO_EMAIL_ID',
    'ac1b973d-5b49-4d0d-a197-865fd25b4a97'
)
CONTACT_OFFICE_AGENT_NOTIFY_TEMPLATE_ID = env.str(
    'CONTACT_OFFICE_AGENT_NOTIFY_TEMPLATE_ID',
    '0492eb2b-7daf-4b37-99cd-be3abbb9eb32'
)
CONTACT_OFFICE_USER_NOTIFY_TEMPLATE_ID = env.str(
    'CONTACT_OFFICE_USER_NOTIFY_TEMPLATE_ID',
    '03c031e1-1ee5-43f9-8b24-f6e4cfd56cf1'
)

CONTACT_ENQUIRIES_AGENT_NOTIFY_TEMPLATE_ID = env.str(
    'CONTACT_ENQUIRIES_AGENT_NOTIFY_TEMPLATE_ID',
    '7a343ec9-7670-4813-9ed4-ae83d3e1f5f7'
)
CONTACT_ENQUIRIES_AGENT_EMAIL_ADDRESS = env.str(
    'CONTACT_ENQUIRIES_AGENT_EMAIL_ADDRESS',
)
CONTACT_ENQUIRIES_USER_NOTIFY_TEMPLATE_ID = env.str(
    'CONTACT_ENQUIRIES_USER_NOTIFY_TEMPLATE_ID',
    '61c82be6-b140-46fc-aeb2-472df8a94d35'
)
CONTACT_EXPORTING_AGENT_SUBJECT = env.str(
    'CONTACT_EXPORTING_AGENT_SUBJECT', 'A form was submitted on great.gov.uk'
)

CONTACT_EXPORTING_TO_UK_HMRC_URL = env.str(
    'CONTACT_EXPORTING_TO_UK_HRMC_URL',
    'https://www.tax.service.gov.uk/shortforms/form/CITEX_CGEF'
)

CONTACT_DEFRA_AGENT_NOTIFY_TEMPLATE_ID = env.str(
    'CONTACT_DEFRA_AGENT_NOTIFY_TEMPLATE_ID',
    '8823e0be-773e-42b0-8dad-740c94d439d4'
)
CONTACT_DEFRA_AGENT_EMAIL_ADDRESS = env.str(
    'CONTACT_DEFRA_AGENT_EMAIL_ADDRESS',
)
CONTACT_DEFRA_USER_NOTIFY_TEMPLATE_ID = env.str(
    'CONTACT_DEFRA_USER_NOTIFY_TEMPLATE_ID',
    '05d70d9f-76a6-4c2f-9f62-6ed4154d6dd6'
)
CONTACT_BEIS_AGENT_NOTIFY_TEMPLATE_ID = env.str(
    'CONTACT_BEIS_AGENT_NOTIFY_TEMPLATE_ID',
    '8823e0be-773e-42b0-8dad-740c94d439d4'
)
CONTACT_BEIS_AGENT_EMAIL_ADDRESS = env.str(
    'CONTACT_BEIS_AGENT_EMAIL_ADDRESS',
)
CONTACT_BEIS_USER_NOTIFY_TEMPLATE_ID = env.str(
    'CONTACT_BEIS_USER_NOTIFY_TEMPLATE_ID',
    'cdc770d8-30e0-42fc-bf11-12385cb40845'
)


# Market Access
MARKET_ACCESS_ZENDESK_SUBJECT = env.str(
    'MARKET_ACCESS_ZENDESK_SUBJECT', 'market access'
)
MARKET_ACCESS_FORMS_API_ZENDESK_SEVICE_NAME = env.str(
    'MARKET_ACCESS_FORMS_API_ZENDESK_SEVICE_NAME', 'market_access'
)

# Community
COMMUNITY_ENQUIRIES_USER_NOTIFY_TEMPLATE_ID = env.str(
    'COMMUNITY_ENQUIRIES_USER_NOTIFY_TEMPLATE_ID',
    'b1a0f719-b00d-4fc4-bc4d-b68ccc50c651'
)
COMMUNITY_ENQUIRIES_AGENT_NOTIFY_TEMPLATE_ID = env.str(
    'COMMUNITY_ENQUIRIES_AGENT_NOTIFY_TEMPLATE_ID',
    '63748451-6dbf-40ea-90b1-05f1f62c61ac'
)
COMMUNITY_ENQUIRIES_AGENT_EMAIL_ADDRESS = env.str(
    'COMMUNITY_ENQUIRIES_AGENT_EMAIL_ADDRESS',
)

# UKEF CONTACT FORM
UKEF_CONTACT_USER_NOTIFY_TEMPLATE_ID = env.str(
    'UKEF_CONTACT_USER_NOTIFY_TEMPLATE_ID',
    '09677460-1796-4a60-a37c-c1a59068219e'
)
UKEF_CONTACT_AGENT_NOTIFY_TEMPLATE_ID = env.str(
    'UKEF_CONTACT_AGENT_NOTIFY_TEMPLATE_ID',
    'e24ba486-6337-46ce-aba3-45d1d3a2aa66'
)
UKEF_CONTACT_AGENT_EMAIL_ADDRESS = env.str(
    'UKEF_CONTACT_AGENT_EMAIL_ADDRESS',
)

LANDING_PAGE_VIDEO_URL = env.str(
    'LANDING_PAGE_VIDEO_URL',
    'https://s3-eu-west-1.amazonaws.com/public-directory-api/'
    'promo-video_web-stitch.mp4'
)

# Activity Stream API
ACTIVITY_STREAM_API_SECRET_KEY = env.str('ACTIVITY_STREAM_API_SECRET_KEY')
ACTIVITY_STREAM_API_ACCESS_KEY = env.str('ACTIVITY_STREAM_API_ACCESS_KEY')
ACTIVITY_STREAM_API_URL = env.str('ACTIVITY_STREAM_API_URL')
ACTIVITY_STREAM_API_IP_WHITELIST = env.str('ACTIVITY_STREAM_API_IP_WHITELIST')

# Export vouchers
EXPORT_VOUCHERS_GOV_NOTIFY_TEMPLATE_ID = env.str(
    'EXPORT_VOUCHERS_GOV_NOTIFY_TEMPLATE_ID', 'c9d3ce3a-236a-4d80-a791-a85dbc6ed377'
)
EXPORT_VOUCHERS_AGENT_EMAIL = env.str('EXPORT_VOUCHERS_AGENT_EMAIL')

# Required by directory components (https://github.com/uktrade/directory-components/pull/286/files)
# These cookies are not used in domestic
LANGUAGE_COOKIE_SECURE = env.bool('LANGUAGE_COOKIE_SECURE', True)
COUNTRY_COOKIE_SECURE = env.bool('COUNTRY_COOKIE_SECURE', True)

# Authentication
AUTH_USER_MODEL = 'sso.SSOUser'
AUTHENTICATION_BACKENDS = ['directory_sso_api_client.backends.SSOUserBackend']
