from importlib import import_module, reload
import sys

import pytest

from django.urls import clear_url_caches, reverse
from django.urls.exceptions import NoReverseMatch


def reload_urlconf(settings):
    clear_url_caches()
    if settings.ROOT_URLCONF in sys.modules:
        reload(sys.modules[settings.ROOT_URLCONF])
    else:
        import_module(settings.ROOT_URLCONF)


def test_international_trade_redirect_feature_off(settings):
    settings.FEATURE_FLAGS['GREAT_INTERNATIONAL_REDIRECTS_ON'] = False
    reload_urlconf(settings)

    with pytest.raises(NoReverseMatch):
        reverse('international-trade-home')


def test_international_trade_redirect_feature_on(settings):
    settings.FEATURE_FLAGS['GREAT_INTERNATIONAL_REDIRECTS_ON'] = True
    reload_urlconf(settings)

    assert reverse('international-trade-home')
