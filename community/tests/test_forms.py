import pytest

from community import forms


def test_community_join_validation_success(community_join_valid_data):
    form = forms.CommunityJoinForm(data=community_join_valid_data)
    assert form.is_valid()
    assert form.cleaned_data == community_join_valid_data


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
def test_community_join_validation_errors(
        invalid_data, invalid_field, error_message
):
    form = forms.CommunityJoinForm(data=invalid_data)
    assert not form.is_valid()
    assert invalid_field in form.errors
    assert form.errors[invalid_field][0] == error_message
