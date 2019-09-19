import pytest
from requests.exceptions import HTTPError

from core.tests.helpers import create_response
from sso import models


def test_retrieve_company_profile_mixin_success(company_profile):
    company_profile.return_value = create_response({'key': 'value'})
    user = models.SSOUser()
    assert user.company == {'key': 'value'}


def test_retrieve_company_profile_mixin_not_ok(company_profile):
    company_profile.return_value = create_response(status_code=502)
    user = models.SSOUser()
    with pytest.raises(HTTPError):
        user.company
