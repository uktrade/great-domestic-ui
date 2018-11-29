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
from directory_components.constants import IP_RETRIEVER_NAME_GOV_UK
from directory_constants.constants import cms


env = environ.Env()
env.read_env()

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
    'finance',
    'directory_healthcheck',
    'health_check',
    'captcha',
    'export_elements',
    'directory_components',
    'prototype',
    'euexit',
    'contact',
]

MIDDLEWARE_CLASSES = [
    'directory_components.middleware.MaintenanceModeMiddleware',
    'directory_components.middleware.IPRestrictorMiddleware',
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
                'directory_components.context_processors.feature_flags',
                'directory_components.context_processors.analytics',
                'directory_components.context_processors.cookie_notice',
                'prototype.context_processors.prototype_home_link',
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
        'LOCATION': 'unique-snowflake',
    }
}

if env.str('REDIS_URL', ''):
    CACHES['cms_fallback'] = {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env.str('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': "django_redis.client.DefaultClient",
        }
    }
    CACHES['api_fallback'] = {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env.str('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': "django_redis.client.DefaultClient",
        }
    }
else:
    CACHES['cms_fallback'] = {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
    CACHES['api_fallback'] = {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
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
DIRECTORY_API_CLIENT_BASE_URL = env.str('API_CLIENT_BASE_URL')
DIRECTORY_API_CLIENT_API_KEY = env.str('API_SIGNATURE_SECRET')
DIRECTORY_API_CLIENT_SENDER_ID = 'directory'
DIRECTORY_API_CLIENT_DEFAULT_TIMEOUT = 15

# directory-sso-proxy
DIRECTORY_SSO_API_CLIENT_BASE_URL = env.str('SSO_API_CLIENT_BASE_URL')
DIRECTORY_SSO_API_CLIENT_API_KEY = env.str('SSO_SIGNATURE_SECRET')
DIRECTORY_SSO_API_CLIENT_SENDER_ID = 'directory'
DIRECTORY_SSO_API_CLIENT_DEFAULT_TIMEOUT = 15
SSO_PROXY_LOGIN_URL = env.str('SSO_PROXY_LOGIN_URL')
SSO_PROXY_LOGOUT_URL = env.str('SSO_PROXY_LOGOUT_URL')
SSO_PROXY_SIGNUP_URL = env.str('SSO_PROXY_SIGNUP_URL')
SSO_PROFILE_URL = env.str('SSO_PROFILE_URL')
SSO_PROXY_REDIRECT_FIELD_NAME = env.str('SSO_PROXY_REDIRECT_FIELD_NAME')
SSO_SESSION_COOKIE = env.str('SSO_SESSION_COOKIE')

ANALYTICS_ID = os.getenv("ANALYTICS_ID")

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
HEADER_FOOTER_URLS_FEEDBACK = env.str('HEADER_FOOTER_URLS_FEEDBACK', '')
HEADER_FOOTER_URLS_DIT = env.str('HEADER_FOOTER_URLS_DIT', '')
COMPONENTS_URLS_FAS = env.str('COMPONENTS_URLS_FAS', '')
PRIVACY_COOKIE_DOMAIN = os.getenv('PRIVACY_COOKIE_DOMAIN')

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

LANDING_PAGE_VIDEO_URL = env.str(
    'LANDING_PAGE_VIDEO_URL',
    (
        'https://s3-eu-west-1.amazonaws.com/public-directory-api/'
        'promo-video_web.mp4'
    )
)

# directory CMS
DIRECTORY_CMS_API_CLIENT_BASE_URL = env.str('CMS_URL')
DIRECTORY_CMS_API_CLIENT_API_KEY = env.str('CMS_SIGNATURE_SECRET')
DIRECTORY_CMS_API_CLIENT_SENDER_ID = 'directory'
DIRECTORY_CMS_API_CLIENT_SERVICE_NAME = cms.EXPORT_READINESS
DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT = 15

# directory clients
DIRECTORY_CLIENT_CORE_CACHE_EXPIRE_SECONDS = 60 * 60 * 24 * 30  # 30 days

FEATURE_CMS_ENABLED = os.getenv('FEATURE_CMS_ENABLED', 'false') == 'true'
FEATURE_PERFORMANCE_DASHBOARD_ENABLED = os.getenv(
    'FEATURE_PERFORMANCE_DASHBOARD_ENABLED', 'false') == 'true'


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
    'PROTOTYPE_PAGES_ON': env.bool(
        'FEATURE_PROTOTYPE_PAGES_ENABLED', False),
    'CAMPAIGN_PAGES_ON': env.bool(
        'FEATURE_CAMPAIGN_PAGES_ENABLED', False),
    'PROTOTYPE_HEADER_FOOTER_ON': env.bool(
        'FEATURE_PROTOTYPE_HEADER_FOOTER_ENABLED', False),
    'NEWS_SECTION_ON': env.bool(
        'FEATURE_NEWS_SECTION_ENABLED', False),
    'INTERNAL_CH_ON': env.bool('FEATURE_USE_INTERNAL_CH_ENABLED', False),
    'UKEF_LEAD_GENERATION_ON': env.bool(
        'FEATURE_UKEF_LEAD_GENERATION_ENABLED', False
    ),
    'PERFORMANCE_DASHBOARD_ON': env.bool(
        'FEATURE_PERFORMANCE_DASHBOARD_ENABLED', False
    ),
    'CONTACT_US_ON': env.bool('FEATURE_CONTACT_US_ENABLED', False),
    # used by directory-components
    'SEARCH_ENGINE_INDEXING_OFF': env.bool(
        'FEATURE_SEARCH_ENGINE_INDEXING_DISABLED', False
    ),
    # used by directory-components
    'MAINTENANCE_MODE_ON': env.bool('FEATURE_MAINTENANCE_MODE_ENABLED', False),
    'EU_EXIT_FORMS_ON': env.bool('FEATURE_EU_EXIT_FORMS_ENABLED', False),
}

PROTOTYPE_HOME_LINK = env.str(
    'PROTOTYPE_HOME_LINK', '/prototype')

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
    'DIRECTORY_FORMS_API_ZENDESK_SEVICE_NAME', 'Directory'
)

# EU exit
EU_EXIT_ZENDESK_SUBDOMAIN = env.str('EU_EXIT_ZENDESK_SUBDOMAIN')
DIRECTORY_FORMS_API_API_KEY_EUEXIT = env.str(
    'DIRECTORY_FORMS_API_API_KEY_EUEXIT'
)
DIRECTORY_FORMS_API_SENDER_ID_EUEXIT = env.str(
    'DIRECTORY_FORMS_API_SENDER_ID_EUEXIT'
)
EUEXIT_AGENT_EMAIL = env.str('EUEXIT_AGENT_EMAIL')
EUEXIT_GOV_NOTIFY_TEMPLATE_ID = env.str(
    'EUEXIT_GOV_NOTIFY_TEMPLATE_ID',
    '15fa965f-2699-4656-a3ee-f087fb53c523'
)
EUEXIT_GOV_NOTIFY_REPLY_TO_ID = env.str('EUEXIT_GOV_NOTIFY_REPLY_TO_ID', None)

# Contact
INVEST_CONTACT_URL = env.str(
    'INVEST_CONTACT_URL', 'https://invest.great.gov.uk/contact/'
)
FIND_A_SUPPLIER_CONTACT_URL = env.str(
    'FIND_A_SUPPLIER_CONTACT_URL',
    'https://trade.great.gov.uk/industries/contact/'
)
FIND_TRADE_OFFICE_URL = env.str(
    'FIND_TRADE_OFFICE_URL',
    'https://www.contactus.trade.gov.uk/office-finder'
)
CONTACT_DOMESTIC_ZENDESK_SUBJECT = env.str(
    'CONTACT_DOMESTIC_ZENDESK_SUBJECT', 'great.gov.uk contact form'
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
CONTACT_EXPORTING_AGENT_SUBJECT = env.str(
    'CONTACT_EXPORTING_AGENT_SUBJECT', 'A form was submitted on great.gov.uk'
)

# ip-restrictor
RESTRICT_ADMIN = env.bool('IP_RESTRICTOR_RESTRICT_IPS', False)
ALLOWED_ADMIN_IPS = env.list('IP_RESTRICTOR_ALLOWED_ADMIN_IPS', default=[])
ALLOWED_ADMIN_IP_RANGES = env.list(
    'IP_RESTRICTOR_ALLOWED_ADMIN_IP_RANGES', default=[]
)
RESTRICTED_APP_NAMES = ['admin', '']
REMOTE_IP_ADDRESS_RETRIEVER = env.str(
    'IP_RESTRICTOR_REMOTE_IP_ADDRESS_RETRIEVER',
    IP_RETRIEVER_NAME_GOV_UK
)
