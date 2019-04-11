from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.utils import translation

from core import middleware


def test_locale_middleware_installed():
    assert all(setting in settings.MIDDLEWARE_CLASSES for setting in (
        'directory_components.middleware.LocaleQuerystringMiddleware',
        'directory_components.middleware.PersistLocaleMiddleware',
        'directory_components.middleware.ForceDefaultLocale',
    ))


def test_locale_middleware_sets_querystring_language(rf):
    request = rf.get(reverse('landing-page-international'), {'lang': 'en-gb'})
    instance = middleware.LocaleQuerystringMiddleware()

    instance.process_request(request)

    expected = 'en-gb'
    assert request.LANGUAGE_CODE == expected == translation.get_language()


def test_locale_middleware_ignored_invalid_querystring_language(rf):
    request = rf.get(reverse('landing-page-international'), {'lang': 'plip'})
    instance = middleware.LocaleQuerystringMiddleware()

    instance.process_request(request)

    expected = settings.LANGUAGE_CODE
    assert request.LANGUAGE_CODE == expected == translation.get_language()


def test_locale_middleware_handles_missing_querystring_language(rf):
    request = rf.get(reverse('landing-page-international'))
    instance = middleware.LocaleQuerystringMiddleware()

    instance.process_request(request)

    expected = settings.LANGUAGE_CODE
    assert request.LANGUAGE_CODE == expected == translation.get_language()


def test_locale_persist_middleware_handles_no_explicit_language(client, rf):
    request = rf.get(reverse('landing-page-international'))
    response = HttpResponse()
    request.session = client.session
    instance = middleware.PersistLocaleMiddleware()

    instance.process_response(request, response)

    cookie = response.cookies[settings.LANGUAGE_COOKIE_NAME]
    assert cookie.value == settings.LANGUAGE_CODE


def test_locale_persist_middleware_persists_explicit_language(client, rf):
    language_code = 'en-gb'
    request = rf.get(
        reverse('landing-page-international'), {'lang': language_code}
    )
    response = HttpResponse()
    request.session = client.session
    instance = middleware.PersistLocaleMiddleware()

    instance.process_response(request, response)
    cookie = response.cookies[settings.LANGUAGE_COOKIE_NAME]

    assert cookie.value == language_code


def test_force_default_locale_sets_to_english(rf, settings):
    request = rf.get(reverse('landing-page-international'))
    instance = middleware.ForceDefaultLocale()

    translation.activate('de')

    assert translation.get_language() == 'de'
    instance.process_request(request)
    assert translation.get_language() == settings.LANGUAGE_CODE


def test_force_default_locale_sets_to_prevous_on_exception(rf):
    request = rf.get(reverse('landing-page-international'))
    request.LANGUAGE_CODE = 'de'
    instance = middleware.ForceDefaultLocale()

    translation.activate('de')
    assert translation.get_language() == 'de'

    instance.process_request(request)
    assert translation.get_language() == settings.LANGUAGE_CODE

    instance.process_exception(request, None)
    assert translation.get_language() == 'de'


def test_force_default_locale_sets_to_prevous_on_response(rf):
    request = rf.get(reverse('landing-page-international'))
    request.LANGUAGE_CODE = 'de'
    instance = middleware.ForceDefaultLocale()

    translation.activate('de')
    assert translation.get_language() == 'de'

    instance.process_request(request)
    assert translation.get_language() == settings.LANGUAGE_CODE

    instance.process_response(request, None)
    assert translation.get_language() == 'de'
