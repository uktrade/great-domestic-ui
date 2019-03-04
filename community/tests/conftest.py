import pytest


@pytest.fixture
def community_valid_form_data(captcha_stub):
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
        'g-recaptcha-response': captcha_stub,
    }
