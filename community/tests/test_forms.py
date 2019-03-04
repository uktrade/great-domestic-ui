import pytest

from community import forms
from community import constants


def test_community_form_validations(valid_community_form_data):
    form = forms.CommunityJoinForm(data=valid_community_form_data)
    assert form.is_valid()
    assert form.cleaned_data['name'] == community_valid_form_data['name']
    assert form.cleaned_data['email'] == community_valid_form_data['email']

    # validate the form with blank 'company_website' field
    valid_community_form_data['company_website'] = ''
    form = forms.CommunityJoinForm(data=valid_community_form_data)
    assert form.is_valid()
    assert form.cleaned_data['name'] == community_valid_form_data['name']
    assert form.cleaned_data['email'] == community_valid_form_data['email']
    assert form.cleaned_data['company_website'] == ''


def test_community_form_api_serialization(
        valid_community_form_data, serialized_community_form_api_data
):
    form = forms.CommunityJoinForm(data=valid_community_form_data)
    assert form.is_valid()

    api_data = form.serialized_data
    sector_label = dict(constants.COMPANY_SECTOR_CHOISES).get(
        form.serialized_data['sector']
    )
    assert api_data['sector_label'] == sector_label
    employees_number_label = dict(constants.EMPLOYEES_NUMBER_CHOISES).get(
        form.serialized_data['employees_number']
    )
    assert api_data['employees_number_label'] == employees_number_label


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
            'name',
            'Enter your full name'
        ),
        (
            {
                'name': 'Test name',
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
                'name': 'Test name',
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
            'Phone number must be entered in the format:'
            ' "+999999999". Up to 15 digits allowed'
        ),
        (
            {
                'name': 'Test name',
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
            'Enter a UK telephone number'
        ),
    )
)
def test_community_form_validation_errors(
        invalid_data, invalid_field, error_message
):
    form = forms.CommunityJoinForm(data=invalid_data)
    assert not form.is_valid()
    assert invalid_field in form.errors
    assert form.errors[invalid_field][0] == error_message
