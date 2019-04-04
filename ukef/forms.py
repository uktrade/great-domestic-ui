from captcha.fields import ReCaptchaField
from django.forms import Select, Textarea
from django.utils.translation import ugettext_lazy as _

from directory_constants.constants.choices import COUNTRY_CHOICES
from directory_forms_api_client.forms import GovNotifyActionMixin
from directory_components.forms import Form
from directory_components import fields, widgets

from contact.forms import TERMS_LABEL

COUNTRIES = COUNTRY_CHOICES.copy()
COUNTRIES.insert(0, ('', 'Select a country'))


class UKEFContactForm(GovNotifyActionMixin, Form):
    full_name = fields.CharField(
        label=_('Full name'),
        min_length=2,
        max_length=50,
        error_messages={
            'required': _('Enter your full name')
        }
    )
    job_title = fields.CharField(
        label=_('Job title'),
        max_length=50,
        error_messages={
            'required': _('Enter your job title'),
        }
    )
    email = fields.EmailField(
        label=_('Business email address'),
        error_messages={
            'required': _('Enter an email address in the correct format,'
                          ' like name@example.com'),
            'invalid': _('Enter an email address in the correct format,'
                         ' like name@example.com'),
        }
    )
    business_name = fields.CharField(
        label=_('Business name'),
        max_length=50,
        error_messages={
            'required': _('Enter your business name'),
        }
    )
    business_website = fields.CharField(
        label=_('Business website'),
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
    country = fields.ChoiceField(
        label=_('Country'),
        widget=Select(),
        choices=COUNTRIES
    )
    like_to_discuss = fields.ChoiceField(
        label=_('Do you have a specific project or proposal you’d like to discuss?'),
        choices=(
            ('no', 'No'),
            ('yes', 'Yes'),
        ),
        widget=widgets.RadioSelect,
        error_messages={'required': _('Please answer this question')}
    )
    like_to_discuss_other = fields.ChoiceField(
        label=_('Which country is the project located in?'),
        widget=Select(),
        choices=COUNTRIES,
        required=False
    )
    how_can_we_help = fields.CharField(
        label=_('How can we help?'),
        help_text=_('Please tell us briefly what type of support you’re looking for'),
        widget=Textarea
    )
    terms_agreed = fields.BooleanField(
        label=TERMS_LABEL,
        error_messages={
            'required': _('You must agree to the terms and conditions'
                          ' before registering'),
        }
    )
    captcha = ReCaptchaField(
        label='',
        label_suffix='',
        error_messages={
            'required': _('Check the box to confirm that you’re human')
        }
    )

    @property
    def serialized_data(self):
        data = super().serialized_data
        if data.get('like_to_discuss_other'):
            like_to_discuss_country = data.get('like_to_discuss_other')
        else:
            like_to_discuss_country = data.get('like_to_discuss_other')
        data['like_to_discuss'] = like_to_discuss_country
        return data


