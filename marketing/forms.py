import re

from captcha.fields import ReCaptchaField
from directory_forms_api_client.forms import GovNotifyActionMixin
from directory_components.forms import Form
from directory_components import fields, widgets
from django.forms import TextInput, forms
from django.utils.translation import ugettext_lazy as _

from marketing import constants as choices
from contact.forms import TERMS_LABEL


class MarketingJoinForm(GovNotifyActionMixin, Form):
    name = fields.CharField(
        label=_('Full name'),
        min_length=2,
        max_length=50,
        error_messages={
            'required': _('Enter your full name')
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
    phone_number_regex = re.compile(r'^(\+\d{1,3}[- ]?)?\d{8,16}$')
    phone_number = fields.CharField(
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
    job_title = fields.CharField(
        label=_('Job title'),
        max_length=50,
        error_messages={
            'required': _('Enter your job title'),
        }
    )
    company_postcode = fields.CharField(
        label=_('Business postcode'),
        max_length=50,
        error_messages={
            'required': _('Enter your business postcode'),
        }
    )
    annual_turnover = fields.ChoiceField(
            label=_('Annual turnover'),
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
    company_location = fields.CharField(
        label=_('Business  location'),
        max_length=50,
        error_messages={
            'required': _('Enter your business location'),
        }
    )
    sector = fields.ChoiceField(
        label=_('Sector'),
        choices=choices.COMPANY_SECTOR_CHOICES,
        error_messages={
            'required': _('Choose a sector'),
        }
    )
    sector_other = fields.CharField(
        label=_('Please specify'),
        widget=TextInput(attrs={'class': 'js-field-other'}),
        required=False,
    )
    company_website = fields.CharField(
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
    employees_number = fields.ChoiceField(
        label=_('Number of employees'),
        choices=choices.EMPLOYEES_NUMBER_CHOICES,
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
    advertising_feedback_other = fields.CharField(
        label=_('Please specify'),
        widget=TextInput(attrs={'class': 'js-field-other'}),
        required=False,
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
        }
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get(
            'phone_number', ''
        ).replace(' ', '')
        if not self.phone_number_regex.match(phone_number):
            raise forms.ValidationError(_('Please enter an UK phone number'))
        return phone_number

    @property
    def serialized_data(self):
        data = super().serialized_data
        sector_mapping = dict(choices.COMPANY_SECTOR_CHOICES)
        employees_number_mapping = dict(choices.EMPLOYEES_NUMBER_CHOICES)
        # advertising_feedback_mapping = dict(choices.HEARD_ABOUT_CHOICES)
        if data.get('sector_other'):
            sector_label = data.get('sector_other')
        else:
            sector_label = sector_mapping.get(data['sector'])
        data['sector_label'] = sector_label
        if data.get('advertising_feedback_other'):
            advertising_feedback_label = data.get('advertising_feedback_other')
        # else:
        #     advertising_feedback_label = advertising_feedback_mapping.get(
        #         data['advertising_feedback']
        #     )
        # data['advertising_feedback_label'] = advertising_feedback_label
        # data['employees_number_label'] = employees_number_mapping.get(
        #     data['employees_number']
        # )
        return data
