import pytest


@pytest.fixture
def valid_community_form_data(captcha_stub):
    return {
        'name': 'Test name',
        'email': 'test@test.com',
        'phone_number': '+447500192913',
        'company_name': 'Limited',
        'company_location': 'London',
        'sector': '3',
        'company_website': 'limitedgoal.com',
        'employees_number': '1',
        'currently_export': 'no',
        'advertising_feedback': '4',
        'terms_agreed': True,
    }


@pytest.fixture
def serialized_community_form_api_data(captcha_stub):
    return {
        'name': 'Test name',
        'email': 'test@test.com',
        'phone_number': '+447500192913',
        'company_name': 'Limited',
        'company_location': 'London',
        'sector': 'Aid Funded Business',
        'company_website': 'limitedgoal.com',
        'employees_number': '10 to 49',
        'currently_export': 'no',
        'advertising_feedback': 'On great.gov.uk',
        'terms_agreed': True,
    }
