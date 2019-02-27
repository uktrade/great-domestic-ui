from directory_forms_api_client.forms import GovNotifyActionMixin
from django import forms
from django.core.validators import RegexValidator

from contact.forms import SerializeDataMixin
from core.constants import HEARD_ABOUT_CHOISES, COMPANY_SECTOR_CHOISES, EMPLOYEES_NUMBER_CHOISES


class CompaniesHouseSearchForm(forms.Form):
    term = forms.CharField()


class CommunityJoinForm(
    SerializeDataMixin, GovNotifyActionMixin, forms.Form
):
    name = forms.CharField(min_length=2, max_length=50)
    email = forms.EmailField()
    phone_number = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format:"
                        " '+999999999'. Up to 15 digits allowed."
            )
        ],
        max_length=17
    )
    company_name = forms.CharField(max_length=50)
    company_location = forms.CharField(max_length=50)
    sector = forms.ChoiceField(choices=COMPANY_SECTOR_CHOISES)
    company_website = forms.CharField(max_length=255)
    employees_number = forms.ChoiceField(choices=EMPLOYEES_NUMBER_CHOISES)
    currently_export = forms.BooleanField()
    advertising_feedback = forms.ChoiceField(choices=HEARD_ABOUT_CHOISES)
