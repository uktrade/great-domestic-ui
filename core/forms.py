from directory_forms_api_client.forms import GovNotifyActionMixin
from directory_components.forms import Form
from directory_components import fields, widgets
from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

from core.constants import HEARD_ABOUT_CHOISES, COMPANY_SECTOR_CHOISES, \
    EMPLOYEES_NUMBER_CHOISES


class CompaniesHouseSearchForm(forms.Form):
    term = forms.CharField()


class CommunityJoinForm(GovNotifyActionMixin, Form):
    name = fields.CharField(
        label=_('Full Name'),
        min_length=2,
        max_length=50,
        error_messages={
            'required': _('Enter your full name')
        }
    )
    email = fields.EmailField(
        label=_('Email address'),
        error_messages={
            'required': _('Enter an email address in the correct format, like name@example.com'), # noqa
            'invalid': _('Enter an email address in the correct format, like name@example.com'),  # noqa
        }
    )
    phone_number = fields.CharField(
        label=_('UK telephone number'),
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format:"
                        " '+999999999'. Up to 15 digits allowed."
            )
        ],
        max_length=15,
        min_length=8,
        help_text=_('This can be a landline or mobile number'),
        error_messages={
            'max_length': _('Figures only, maximum 15 characters, minimum 8 characters excluding spaces'), # noqa
            'min_length': _('Figures only, maximum 15 characters, minimum 8 characters excluding spaces'), # noqa
            'required': _('Enter a UK telephone number'),
            'invalid': _('Enter a UK telephone number')
        }
    )
    company_name = fields.CharField(
        label=_('Business name'),
        max_length=50,
        error_messages={
            'required': _('Enter your business name'),
        }
    )
    company_location = fields.CharField(
        label=_('Business  location'),
        max_length=50,
        error_messages={
            'required': _('Enter your business location'),
        }
    )
    sector = fields.ChoiceField(
        choices=COMPANY_SECTOR_CHOISES,
        error_messages={
            'required': _('Choose a sector'),
        }
    )
    company_website = fields.CharField(
        max_length=255,
        help_text=_('Enter the home page address'),
        error_messages={
            'required': _('Enter a website address in the correct format, '
                          'like https://www.example.com or www.company.com'),
            'invalid': _('Enter a website address in the correct format, '
                         'like https://www.example.com or www.company.com')
        }
    )
    employees_number = fields.ChoiceField(
        choices=EMPLOYEES_NUMBER_CHOISES,
        error_messages={
            'required': _('Choose a number'),
        }
    )
    currently_export = fields.ChoiceField(
            label=_('Do you currently export?'),
            choices=(
                ('yes', 'Yes'),
                ('no', 'No')
            ),
            widget=widgets.RadioSelect
    )
    advertising_feedback = fields.ChoiceField(
        choices=HEARD_ABOUT_CHOISES,
        error_messages={
            'required': _('Please tell us where you heard about becoming an Export Advocate'), # noqa
        }
    )
