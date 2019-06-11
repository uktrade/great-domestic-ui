from captcha.fields import ReCaptchaField
from directory_constants import choices, urls
from directory_components import forms, fields, widgets

from django.forms import Textarea, TextInput
from django.utils.html import mark_safe


class CategoryForm(forms.Form):
    error_css_class = 'input-field-container has-error'

    CATEGORY_CHOICES = (
        'Securing upfront funding',
        'Offering competitive but secure payment terms',
        'Guidance on export finance and insurance',
    )
    categories = fields.MultipleChoiceField(
        label='',
        widget=widgets.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-multiple'},
            use_nice_ids=True,
        ),
        choices=((choice, choice) for choice in CATEGORY_CHOICES)
    )


class PersonalDetailsForm(forms.Form):
    error_css_class = 'input-field-container has-error'

    firstname = fields.CharField(label='Your first name')
    lastname = fields.CharField(label='Your last name')
    position = fields.CharField(label='Position in company')
    email = fields.EmailField(label='Email address')
    phone = fields.CharField(label='Phone')


class CompanyDetailsForm(forms.Form):

    EXPORT_CHOICES = (
        'I have three years of registered accounts',
        'I have customers outside UK',
        'I supply companies that sell overseas',
    )
    INDUSTRY_CHOICES = [('', '')] + [
        (value.replace('_', ' ').title(), label)
        for (value, label) in choices.INDUSTRIES
    ] + [('Other', 'Other')]

    error_css_class = 'input-field-container has-error'

    trading_name = fields.CharField(label='Registered name')
    company_number = fields.CharField(
        label='Companies House number', required=False
    )
    address_line_one = fields.CharField(label='Building and street')
    address_line_two = fields.CharField(label='', required=False)
    address_town_city = fields.CharField(label='Town or city')
    address_county = fields.CharField(label='County')
    address_post_code = fields.CharField(label='Postcode')
    industry = fields.ChoiceField(
        initial='thing',
        choices=INDUSTRY_CHOICES
    )
    industry_other = fields.CharField(
        label='Type in your industry',
        widget=TextInput(attrs={'class': 'js-field-other'}),
        required=False,
    )

    export_status = fields.MultipleChoiceField(
        label='',
        widget=widgets.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-multiple'},
            use_nice_ids=True,
        ),
        choices=((choice, choice) for choice in EXPORT_CHOICES),
    )

    def clean(self):
        cleaned_data = super().clean()
        return {
            **cleaned_data,
            'not_companies_house': not cleaned_data.get('company_number')
        }


class HelpForm(forms.Form):
    error_css_class = 'input-field-container has-error'

    comment = fields.CharField(
        label='',
        help_text='Tell us about your export experience, including any '
                  'challenges you are facing. We’re particularly '
                  'interested in the markets you have exported to '
                  'and whether you have already spoken to your '
                  'bank or a broker.',
        widget=Textarea,
    )
    terms_agreed = fields.BooleanField(
        label=mark_safe(
            'Tick this box to accept the '
            f'<a href="{urls.TERMS_AND_CONDITIONS}" target="_blank">terms and '
            'conditions</a> of the great.gov.uk service.'
        )
    )
    captcha = ReCaptchaField(label_suffix='')
