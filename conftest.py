import os
from unittest import mock

import pytest

from django.core.cache import cache

from sso.utils import SSOUser


@pytest.fixture(autouse=True)
def clear_django_cache():
    cache.clear()


@pytest.fixture
def dummy_cms_page():
    return {
        'title': 'test',
        'meta': {
            'languages': [
                ['en-gb', 'English'],
            ]
        },
        'page_type': ''
    }


@pytest.fixture
def sso_user():
    return SSOUser(
        id=999,
        email='test@foo.com',
        session_id=1
    )


def process_request(self, request):
    request.sso_user = sso_user()


@pytest.fixture
def authed_client(client):
    stub = mock.patch(
        'sso.middleware.SSOUserMiddleware.process_request', process_request
    )
    stub.start()
    yield client
    stub.stop()


@pytest.fixture()
def captcha_stub():
    # https://github.com/praekelt/django-recaptcha#id5
    os.environ['RECAPTCHA_TESTING'] = 'True'
    yield 'PASSED'
    os.environ['RECAPTCHA_TESTING'] = 'False'


@pytest.fixture(autouse=True)
def feature_flags(settings):
    # solves this issue: https://github.com/pytest-dev/pytest-django/issues/601
    settings.FEATURE_FLAGS = {**settings.FEATURE_FLAGS}
    yield settings.FEATURE_FLAGS
