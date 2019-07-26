import pytest

from marketing import forms
from marketing import constants


def test_marketing_form_validations(valid_marketing_form_data):
    form = forms.MarketingJoinForm(data=valid_marketing_form_data)
    assert form.is_valid()
    assert form.cleaned_data['first_name'] == valid_marketing_form_data['first_name']
    assert form.cleaned_data['email'] == valid_marketing_form_data['email']

    #validate the form with blank 'annual_turnover' field
    valid_marketing_form_data['annual_turnover'] = ''
    form = forms.MarketingJoinForm(data=valid_marketing_form_data)
    assert form.is_valid()
    assert form.cleaned_data['first_name'] == valid_marketing_form_data['first_name']
    assert form.cleaned_data['email'] == valid_marketing_form_data['email']
    assert form.cleaned_data['annual_turnover'] == ''


def test_marketing_form_api_serialization(valid_marketing_form_data):
    form = forms.MarketingJoinForm(data=valid_marketing_form_data)
    assert form.is_valid()
    api_data = form.serialized_data
    employees_number_label = dict(constants.EMPLOYEES_NUMBER_CHOICES).get(
        form.serialized_data['employees_number']
    )
    assert api_data['employees_number_label'] == employees_number_label


def test_marketing_form_api_serialization_with_other_options(
        valid_marketing_form_data_with_other_options
):
    form = forms.MarketingJoinForm(
        data=valid_marketing_form_data_with_other_options
    )
    assert form.is_valid()

#    TO BE UPDATED WITH ANNUAL-TURNOVER


@pytest.mark.parametrize(
    'invalid_data,invalid_field,error_message',
    (
        (
            {
                'email': 'test@test.com',
                'phone_number': '+447500192913',
                'company_name': 'Limited',
                'company_location': 'London',
                'sector': '3',
                'company_website': 'limitedgoal.com',
                'employees_number': '1',
                'currently_export': 'no',
                'advertising_feedback': '4',
            },
            'first_name',
            'Enter your first name'
        ),
        (
            {
                'first_name': 'Test',
                'phone_number': '+447500192913',
                'company_name': 'Limited',
                'company_location': 'London',
                'sector': '3',
                'company_website': 'limitedgoal.com',
                'employees_number': '1',
                'currently_export': 'no',
                'advertising_feedback': '4',
            },
            'email',
            'Enter an email address in the correct format,'
            ' like name@example.com'
        ),
        (
            {
                'first_name': 'Test name',
                'email': 'test@test.com',
                'phone_number': '++00192913',  # invalid field data
                'company_name': 'Limited',
                'company_location': 'London',
                'sector': '3',
                'company_website': 'limitedgoal.com',
                'employees_number': '1',
                'currently_export': 'no',
                'advertising_feedback': '4',
            },
            'phone_number',
            'Please enter an UK phone number'
        ),
        (
            {
                'first_name': 'Test name',
                'email': 'test@test.com',
                'company_name': 'Limited',
                'company_location': 'London',
                'sector': '3',
                'company_website': 'limitedgoal.com',
                'employees_number': '1',
                'currently_export': 'no',
                'advertising_feedback': '4',
            },
            'phone_number',
            'Enter a UK phone number'
        ),
    )
)
def test_marketing_form_validation_errors(
        invalid_data, invalid_field, error_message
):
    form = forms.MarketingJoinForm(data=invalid_data)
    assert not form.is_valid()
    assert invalid_field in form.errors
    assert form.errors[invalid_field][0] == error_message


def test_phone_number_validation(valid_marketing_form_data):
    form = forms.MarketingJoinForm(data=valid_marketing_form_data)
    assert form.is_valid()

    # validate a phone number without country code
    valid_marketing_form_data['phone_number'] = '07501234567'
    form = forms.MarketingJoinForm(data=valid_marketing_form_data)
    assert form.is_valid()

    # # validate a phone number with spaces
    valid_marketing_form_data['phone_number'] = '+44 0750 123 45 67'
    form = forms. MarketingJoinForm(data=valid_marketing_form_data)
    assert form.is_valid()

    # # validate a phone number with country code
    valid_marketing_form_data['phone_number'] = '+447501234567'
    form = forms.MarketingJoinForm(data=valid_marketing_form_data)
    assert form.is_valid()
