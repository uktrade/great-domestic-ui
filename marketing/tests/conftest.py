import pytest


@pytest.fixture
def valid_marketing_form_data(captcha_stub):
    return {
        'first_name': 'Test',
        'last_name': 'Name',
        'email': 'test@test.com',
        'phone_number': '+447501234567',
        'job_title': 'developer',
        'company_name': 'Limited',
        'company_postcode': 'sw1 1bb',
        'employees_number': '1-9',
        'annual_turnover': '',
        'currently_export': 'no',
        'terms_agreed': True,
        'g-recaptcha-response': captcha_stub,
    }


@pytest.fixture
def valid_marketing_form_data_with_other_options(captcha_stub):
    return {
        'first_name': 'Test',
        'last_name': 'Name',
        'email': 'test@test.com',
        'phone_number': '+447501234567',
        'job_title': 'developer',
        'company_name': 'Limited',
        'company_postcode': 'sw1 1bb',
        'employees_number': '1-9',
        'annual_turnover': '',
        'currently_export': 'no',
        'terms_agreed': True,
        'g-recaptcha-response': captcha_stub,
    }


@pytest.fixture
def serialized_marketing_form_api_data(captcha_stub):
    return {
        'first_name': 'Test',
        'last_name': 'Name',
        'email': 'test@test.com',
        'phone_number': '+447501234567',
        'job_title': 'developer',
        'company_name': 'Limited',
        'company_postcode': 'sw1 1bb',
        'employees_number': '1-9',
        'annual_turnover': '',
        'currently_export': 'no',
        'terms_agreed': True,
    }
