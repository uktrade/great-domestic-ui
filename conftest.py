import os
from unittest import mock

import pytest

from django.contrib.auth import get_user_model
from django.core.cache import cache

from core.tests.helpers import create_response


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


@pytest.fixture
def user():
    SSOUser = get_user_model()
    return SSOUser(
        id=1,
        pk=1,
        email='jim@example.com',
        mobile_phone_number='55512345',
        first_name='Jim',
        last_name='Cross',
        session_id='123',
    )

@pytest.fixture(autouse=True)
def auth_backend():
    patch = mock.patch(
        'directory_sso_api_client.sso_api_client.user.get_session_user',
        return_value=create_response(status_code=404)
    )
    yield patch.start()
    patch.stop()


@pytest.fixture
def client(client, auth_backend, settings):
    def force_login(user):
        client.cookies[settings.SSO_SESSION_COOKIE] = '123'
        auth_backend.return_value = create_response({
            'id': user.id,
            'email': user.email,
            'hashed_uuid': user.hashed_uuid,
            'user_profile': {
                'mobile_phone_number': user.mobile_phone_number,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        })
    client.force_login = force_login
    return client


@pytest.fixture(autouse=True)
def company_profile(client, user):
    client.force_login(user)
    response = create_response({
        'company_type': 'COMPANIES_HOUSE',
        'number': 1234567,
        'name': 'Example corp',
        'postal_code': 'Foo Bar',
        'sectors': ['AEROSPACE'],
        'employees': '1-10',
        'mobile_number': '07171771717',
        'postal_full_name': 'Foo Example',
        'address_line_1': '123 Street',
        'address_line_2': 'Near Fake Town',
        'country': 'FRANCE',
        'locality': 'Paris',
        'summary': 'Makes widgets',
        'website': 'http://www.example.com',
    })
    stub = mock.patch('directory_api_client.api_client.company.profile_retrieve', return_value=response)
    yield stub.start()
    stub.stop()
