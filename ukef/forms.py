from django.forms import Select
from django.utils.translation import ugettext_lazy as _

from directory_constants.constants.choices import COUNTRY_CHOICES
from directory_forms_api_client.forms import GovNotifyActionMixin
from directory_components.forms import Form
from directory_components import fields, widgets


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
    business_email = fields.EmailField(
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
        choices=COUNTRY_CHOICES
    )
    #
    # like_to_discuss = fields.BooleanField()
    # how_can_we_help = fields.CharField()
