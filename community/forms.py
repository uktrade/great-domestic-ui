import re

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from directory_forms_api_client.forms import GovNotifyEmailActionMixin
from directory_components.forms import Form
from directory_components import forms
from django.forms import TextInput, ValidationError
from django.utils.translation import ugettext_lazy as _

from community import constants
from contact.forms import TERMS_LABEL
from core.constants import INDUSTRY_CHOICES, INDUSTRY_MAP


class CommunityJoinForm(GovNotifyEmailActionMixin, Form):
    name = forms.CharField(
        label=_('Full name'),
        min_length=2,
        max_length=50,
        error_messages={
            'required': _('Enter your full name')
        }
    )
    email = forms.EmailField(
        label=_('Email address'),
        error_messages={
            'required': _('Enter an email address in the correct format,'
                          ' like name@example.com'),
            'invalid': _('Enter an email address in the correct format,'
                         ' like name@example.com'),
        }
    )
    phone_number_regex = re.compile(r'^(\+\d{1,3}[- ]?)?\d{8,16}$')
    phone_number = forms.CharField(
        label=_('UK telephone number'),
        min_length=8,
        help_text=_('This can be a landline or mobile number'),
        error_messages={
            'max_length': _('Figures only, maximum 16 characters,'
                            ' minimum 8 characters excluding spaces'),
            'min_length': _('Figures only, maximum 16 characters,'
                            ' minimum 8 characters excluding spaces'),
            'required': _('Enter an UK phone number'),
            'invalid': _('Please enter an UK phone number')
        }
    )
    company_name = forms.CharField(
        label=_('Business name'),
        max_length=50,
        error_messages={
            'required': _('Enter your business name'),
        }
    )
    company_location = forms.CharField(
        label=_('Business  location'),
        max_length=50,
        error_messages={
            'required': _('Enter your business location'),
        }
    )
    sector = forms.ChoiceField(
        label=_('Sector'),
        choices=INDUSTRY_CHOICES,
        error_messages={
            'required': _('Choose a sector'),
        }
    )
    sector_other = forms.CharField(
        label=_('Please specify'),
        widget=TextInput(attrs={'class': 'js-field-other'}),
        required=False,
    )
    company_website = forms.CharField(
        label=_('Website'),
        max_length=255,
        help_text=_('Enter the home page address'),
        error_messages={
            'required': _('Enter a website address in the correct format, '
                          'like https://www.example.com or www.company.com'),
            'invalid': _('Enter a website address in the correct format, '
                         'like https://www.example.com or www.company.com')
        },
        required=False
    )
    employees_number = forms.ChoiceField(
        label=_('Number of employees'),
        choices=constants.EMPLOYEES_NUMBER_CHOISES,
        error_messages={
            'required': _('Choose a number'),
        }
    )
    currently_export = forms.ChoiceField(
            label=_('Do you currently export?'),
            choices=(
                ('yes', 'Yes'),
                ('no', 'No')
            ),
            widget=forms.RadioSelect,
            error_messages={'required': _('Please answer this question')}
    )
    advertising_feedback = forms.ChoiceField(
        label=_('Where did you hear about becoming an Export Advocate?'),
        choices=constants.HEARD_ABOUT_CHOISES,
        error_messages={
            'required': _('Please tell us where you heard about'
                          ' becoming an Export Advocate'),
        }
    )
    advertising_feedback_other = forms.CharField(
        label=_('Please specify'),
        widget=TextInput(attrs={'class': 'js-field-other'}),
        required=False,
    )

    terms_agreed = forms.BooleanField(
        label=TERMS_LABEL,
        error_messages={
            'required': _('You must agree to the terms and conditions'
                          ' before registering'),
        }
    )
    captcha = ReCaptchaField(
        label='',
        label_suffix='',
        widget=ReCaptchaV3()
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number', '').replace(' ', '')
        if not self.phone_number_regex.match(phone_number):
            raise ValidationError(_('Please enter an UK phone number'))
        return phone_number

    def clean_employees_number(self):
        value = self.cleaned_data['employees_number']
        self.cleaned_data['employees_number_label'] = constants.EMPLOYEES_NUMBER_MAP[value]
        return value

    def clean_sector_other(self):
        if self.cleaned_data['sector_other']:
            self.cleaned_data['sector_label'] = self.cleaned_data['sector_other']
        return self.cleaned_data['sector_other']

    def clean_advertising_feedback_other(self):
        if self.cleaned_data['advertising_feedback_other']:
            self.cleaned_data['advertising_feedback_label'] = self.cleaned_data['advertising_feedback_other']
        return self.cleaned_data['advertising_feedback_other']

    def clean(self):
        data = super().clean()
        if 'sector_label' not in data and 'sector' in data:
            self.cleaned_data['sector_label'] = INDUSTRY_MAP[data['sector']]
        if 'advertising_feedback_label' not in data and 'advertising_feedback' in data:
            self.cleaned_data['advertising_feedback_label'] = constants.HEARD_ABOUT_MAP[data['advertising_feedback']]
        return data
