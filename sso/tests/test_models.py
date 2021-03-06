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


def test_get_full_name_with_user_details(user):
    user.first_name = "Joe"
    user.last_name = "Bloggs"
    assert user.get_full_name() == "Joe Bloggs"


def test_get_full_name_with_company_details(user, company_profile):
    # This inherits the company_profile fixture with a postal_full_name
    # of Jim Cross
    assert user.get_full_name() == "Jim Cross"


def test_get_full_name_with_no_details(user, company_profile):
    # Inherit the company_profile fixture and overwrite the company
    # information
    user.first_name = ''
    user.last_name = ''
    company_profile.return_value = create_response({})
    assert user.get_full_name() == ''


def test_get_mobile_number_with_user_details(user):
    user.mobile_phone_number = "123"
    assert user.get_mobile_number() == "123"


def test_get_mobile_number_with_company_details(user, company_profile):
    # This inherits the company_profile fixture with a mobile_number
    # of 07171771717
    user.mobile_phone_number = ""
    assert user.get_mobile_number() == "07171771717"


def test_get_mobile_number_with_no_details(user, company_profile):
    # Inherit the company_profile fixture and overwrite the company
    # information
    user.mobile_phone_number = ""
    company_profile.return_value = create_response({})
    assert user.get_mobile_number() == ''
