from directory_forms_api_client.forms import GovNotifyActionMixin
from directory_components.forms import Form
from directory_components import fields, widgets
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

from community import constants as choices
from contact.forms import TERMS_LABEL


class CommunityJoinForm(GovNotifyActionMixin, Form):
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
            'max_length': _('Figures only, maximum 15 characters,'
                            ' minimum 8 characters excluding spaces'),
            'min_length': _('Figures only, maximum 15 characters,'
                            ' minimum 8 characters excluding spaces'),
            'required': _('Enter a UK telephone number'),
            'invalid': _('Phone number must be entered in the format:'
                         ' "+999999999". Up to 15 digits allowed')
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
        label=_('Sector'),
        choices=choices.COMPANY_SECTOR_CHOISES,
        error_messages={
            'required': _('Choose a sector'),
        }
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
        choices=choices.EMPLOYEES_NUMBER_CHOISES,
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
        label=_('Where did you hear about becoming an Export Advocate?'),
        choices=choices.HEARD_ABOUT_CHOISES,
        error_messages={
            'required': _('Please tell us where you heard about'
                          ' becoming an Export Advocate'),
        }
    )

    terms_agreed = fields.BooleanField(label=TERMS_LABEL)

    @property
    def serialized_data(self):
        data = super().serialized_data
        sector_mapping = dict(choices.COMPANY_SECTOR_CHOISES)
        employees_number_mapping = dict(choices.EMPLOYEES_NUMBER_CHOISES)
        advertising_feedback_mapping = dict(choices.HEARD_ABOUT_CHOISES)
        data['sector_label'] = sector_mapping.get(data['sector'])
        data['employees_number_label'] = employees_number_mapping.get(
            data['employees_number']
        )
        data['advertising_feedback_label'] = advertising_feedback_mapping.get(
            data['advertising_feedback']
        )
        return data
