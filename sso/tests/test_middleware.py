from unittest.mock import patch, Mock

import pytest
import requests

from django.core.urlresolvers import reverse

from sso import middleware

from core.middleware import RedirectMiddleware

def api_response_ok(*args, **kwargs):
    return Mock(
        ok=True,
        json=lambda: {
            'id': 1,
            'email': 'jim@example.com',
        }
    )


def api_response_bad():
    return Mock(ok=False)

def redirect_response_ok():
    return Mock({'id': 1, 'target_url': 'https://gov.uk/exit'})

def test_sso_middleware_installed(settings):
    assert 'sso.middleware.SSOUserMiddleware' in settings.MIDDLEWARE_CLASSES


@patch('directory_sso_api_client.client.sso_api_client.user.get_session_user')
def test_sso_middleware_no_cookie(mock_get_session_user, settings, client):
    settings.MIDDLEWARE_CLASSES = ['sso.middleware.SSOUserMiddleware']
    response = client.get(reverse('casestudy-york-bag'))

    mock_get_session_user.assert_not_called()
    assert response._request.sso_user is None


@patch('directory_sso_api_client.client.sso_api_client.user.get_session_user')
def test_sso_middleware_api_response_ok(
    mock_get_session_user, settings, client
):
    mock_get_session_user.return_value = api_response_ok()
    client.cookies[settings.SSO_SESSION_COOKIE] = '123'
    settings.MIDDLEWARE_CLASSES = ['sso.middleware.SSOUserMiddleware']
    response = client.get(reverse('casestudy-york-bag'))

    mock_get_session_user.assert_called_with('123')
    assert response._request.sso_user.id == 1
    assert response._request.sso_user.session_id == '123'
    assert response._request.sso_user.email == 'jim@example.com'


@patch('directory_sso_api_client.client.sso_api_client.user.get_session_user',
       api_response_bad)
def test_sso_middleware_bad_response(settings, client):
    settings.MIDDLEWARE_CLASSES = ['sso.middleware.SSOUserMiddleware']
    response = client.get(reverse('casestudy-york-bag'))

    assert response._request.sso_user is None


def test_redirect_middleware_installed(settings):
    assert 'core.middleware.RedirectMiddleware' in settings.MIDDLEWARE_CLASSES


@patch('directory_api_client.api_client.redirects', redirect_response_ok)
def test_redirect_middleware_response(settings, client):
    settings.MIDDLEWARE_CLASSES = ['core.middleware.RedirectMiddleware']
    response = RedirectMiddleware()

    assert response is not None


@pytest.mark.parametrize(
    'exception_class', requests.exceptions.RequestException.__subclasses__()
)
@patch('directory_sso_api_client.client.sso_api_client.user.get_session_user')
def test_sso_middleware_timeout(
    mock_get_session_user, settings, client, caplog, exception_class
):
    mock_get_session_user.side_effect = exception_class()
    client.cookies[settings.SSO_SESSION_COOKIE] = '123'
    settings.MIDDLEWARE_CLASSES = [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'sso.middleware.SSOUserMiddleware'
    ]

    response = client.get(reverse('about'))

    assert response.status_code == 200

    log = caplog.records[-1]
    assert log.levelname == 'ERROR'
    assert log.msg == middleware.SSOUserMiddleware.MESSAGE_SSO_UNREACHABLE
