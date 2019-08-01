import re

from captcha.fields import ReCaptchaField
from directory_forms_api_client.forms import GovNotifyActionMixin
from directory_components.forms import Form
from directory_components import fields, widgets
from django.forms import forms
from django.utils.translation import ugettext_lazy as _

from marketing import constants as choices
from contact.forms import TERMS_LABEL
from ukpostcodeutils import validation

PHONE_NUMBER_REGEX = re.compile(r'^(\+\d{1,3}[- ]?)?\d{8,16}$')


class MarketingJoinForm(GovNotifyActionMixin, Form):
    first_name = fields.CharField(
        label=_('First name'),
        min_length=2,
        max_length=50,
        error_messages={
            'required': _('Enter your first name')
        }
    )
    last_name = fields.CharField(
        label=_('Last name'),
        min_length=2,
        max_length=50,
        error_messages={
            'required': _('Enter your last name')
        }
    )
    email = fields.EmailField(
        label=_('Email address'),
        error_messages={
            'required': _('Enter an email address in the correct format,'
                          ' like name@example.com'),
            'invalid': _('Enter an email address in the correct format,'
                         ' like name@example.com'),
        }
    )
    phone_number = fields.CharField(
        label=_('UK telephone number'),
        min_length=8,
        help_text=_('This can be a landline or mobile number'),
        error_messages={
            'max_length': _('Figures only, maximum 16 characters,'
                            ' minimum 8 characters excluding spaces'),
            'min_length': _('Figures only, maximum 16 characters,'
                            ' minimum 8 characters excluding spaces'),
            'required': _('Enter a UK phone number'),
            'invalid': _('Please enter a UK phone number')
        }
    )
    job_title = fields.CharField(
        label=_('Job title'),
        max_length=50,
        error_messages={
            'required': _('Enter your job title'),
        }
    )
    company_name = fields.CharField(
        label=_('Business name'),
        max_length=50,
        error_messages={
            'required': _('Enter your business name'),
        }
    )
    company_postcode = fields.CharField(
        label=_('Business postcode'),
        max_length=50,
        error_messages={
            'required': _('Enter your business postcode'),
            'invalid': _('Please enter a UK postcode')
        }
    )
    annual_turnover = fields.ChoiceField(
            label=_('Annual turnover'),
            help_text=_('This information will help us tailor our response and advice on the services we can provide.'),
            choices=(
                ('Less than £500K', 'Less than £500K'),
                ('£500K to £2M', '£500K to £2M'),
                ('£2M to £5M', '£2M to £5M'),
                ('£5M to £10M', '£5M to £10M'),
                ('£10M to £50M', '£10M to £50M'),
                ('£50M or higher', '£50M or higher')
            ),
            widget=widgets.RadioSelect,
            required=False,
    )
    employees_number = fields.ChoiceField(
        label=_('Number of employees'),
        choices=choices.EMPLOYEES_NUMBER_CHOICES,
        widget=widgets.RadioSelect,
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
            widget=widgets.RadioSelect,
            error_messages={'required': _('Please answer this question')}
    )

    terms_agreed = fields.BooleanField(
        label=TERMS_LABEL,
        error_messages={
            'required': _('You must agree to the terms and conditions'
                          ' before registering'),
        }
    )
    captcha = ReCaptchaField(
        label_suffix='',
        error_messages={
            'required': _('Check the box to confirm that you’re human')
        },
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get(
            'phone_number', ''
        ).replace(' ', '')
        if not PHONE_NUMBER_REGEX.match(phone_number):
            raise forms.ValidationError(_('Please enter a UK phone number'))
        return phone_number

    def clean_company_postcode(self):

        company_postcode = self.cleaned_data.get(
            'company_postcode', ''
        ).replace(' ', '').upper()
        if not validation.is_valid_postcode(company_postcode):
            raise forms.ValidationError(_('Please enter a UK postcode'))
        return company_postcode

    @property
    def serialized_data(self):
        data = super().serialized_data
        employees_number_mapping = dict(choices.EMPLOYEES_NUMBER_CHOICES)
        data['employees_number_label'] = employees_number_mapping.get(data['employees_number'])
        return data
