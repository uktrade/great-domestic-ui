from captcha.fields import ReCaptchaField
from directory_constants import choices, urls
from directory_components import forms

from django.forms import Textarea, TextInput
from django.utils.html import mark_safe


class CategoryForm(forms.Form):
    error_css_class = 'input-field-container has-error'

    CATEGORY_CHOICES = (
        'Securing upfront funding',
        'Offering competitive but secure payment terms',
        'Guidance on export finance and insurance',
    )
    categories = forms.MultipleChoiceField(
        label='',
        widget=forms.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-multiple'},
            use_nice_ids=True,
        ),
        choices=((choice, choice) for choice in CATEGORY_CHOICES)
    )


class PersonalDetailsForm(forms.Form):
    error_css_class = 'input-field-container has-error'

    firstname = forms.CharField(label='Your first name')
    lastname = forms.CharField(label='Your last name')
    position = forms.CharField(label='Position in company')
    email = forms.EmailField(label='Email address')
    phone = forms.CharField(label='Phone')


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

    trading_name = forms.CharField(label='Registered name')
    company_number = forms.CharField(
        label='Companies House number', required=False
    )
    address_line_one = forms.CharField(label='Building and street')
    address_line_two = forms.CharField(label='', required=False)
    address_town_city = forms.CharField(label='Town or city')
    address_county = forms.CharField(label='County')
    address_post_code = forms.CharField(label='Postcode')
    industry = forms.ChoiceField(
        initial='thing',
        choices=INDUSTRY_CHOICES
    )
    industry_other = forms.CharField(
        label='Type in your industry',
        widget=TextInput(attrs={'class': 'js-field-other'}),
        required=False,
    )

    export_status = forms.MultipleChoiceField(
        label='',
        widget=forms.CheckboxSelectInlineLabelMultiple(
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

    comment = forms.CharField(
        label='',
        help_text='Tell us about your export experience, including any '
                  'challenges you are facing. We’re particularly '
                  'interested in the markets you have exported to '
                  'and whether you have already spoken to your '
                  'bank or a broker.',
        widget=Textarea,
    )
    terms_agreed = forms.BooleanField(
        label=mark_safe(
            'Tick this box to accept the '
            f'<a href="{urls.TERMS_AND_CONDITIONS}" target="_blank">terms and '
            'conditions</a> of the great.gov.uk service.'
        )
    )
    captcha = ReCaptchaField(label_suffix='')
