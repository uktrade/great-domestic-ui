from captcha.fields import ReCaptchaField
from directory_components import forms, fields, widgets
from directory_constants.constants import choices, urls
from directory_forms_api_client.forms import (
    GovNotifyActionMixin, ZendeskActionMixin
)
import requests.exceptions

from django.conf import settings
from django.forms import Textarea, TextInput, TypedChoiceField, ValidationError
from django.utils.functional import cached_property
from django.utils.html import mark_safe

from contact import constants, helpers
from contact.fields import IntegerField


TERMS_LABEL = mark_safe(
    'Tick this box to accept the '
    f'<a href="{urls.TERMS_AND_CONDITIONS}" target="_blank">terms and '
    'conditions</a> of the great.gov.uk service.'
)

LIMITED = 'LIMITED'

COMPANY_TYPE_CHOICES = (
    (LIMITED, 'UK private or public limited company'),
    ('OTHER', 'Other type of UK organisation'),
)
COMPANY_TYPE_OTHER_CHOICES = (
    ('CHARITY', 'Charity'),
    ('GOVERNMENT_DEPARTMENT', 'Government department'),
    ('INTERMEDIARY', 'Intermediary'),
    ('LIMITED_PARTNERSHIP', 'Limited partnership'),
    ('SOLE_TRADER', 'Sole Trader'),
    ('FOREIGN', 'UK branch of foreign company'),
    ('OTHER', 'Other'),
)
INDUSTRY_CHOICES = (
    (('', 'Please select'),) + choices.INDUSTRIES + (('OTHER', 'Other'),)
)


class EuExitOptionFeatureFlagMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not settings.FEATURE_FLAGS['EU_EXIT_FORMS_ON']:
            self.fields['choice'].choices = [
                (value, label) for value, label in self.CHOICES
                if value != constants.EUEXIT
            ]


class NewUserRegOptionFeatureFlagMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not settings.FEATURE_FLAGS['NEW_REGISTRATION_JOURNEY_ON']:
            self.fields['choice'].choices = [
                (value, label) for value, label in self.CHOICES
                if value != constants.COMPANY_NOT_FOUND
            ]


class NoOpForm(forms.Form):
    pass


class SerializeDataMixin:

    @property
    def serialized_data(self):
        data = self.cleaned_data.copy()
        del data['captcha']
        del data['terms_agreed']
        return data


class LocationRoutingForm(forms.Form):
    CHOICES = (
        (constants.DOMESTIC, 'The UK'),
        (constants.INTERNATIONAL, 'Outside the UK'),
    )
    choice = fields.ChoiceField(
        label='',
        widget=widgets.RadioSelect(),
        choices=CHOICES,
    )


class DomesticRoutingForm(EuExitOptionFeatureFlagMixin, forms.Form):

    CHOICES = (
        (constants.TRADE_OFFICE, 'Find your local trade office'),
        (constants.EXPORT_ADVICE, 'Advice to export from the UK'),
        (
            constants.GREAT_SERVICES,
            'great.gov.uk account and services support'
        ),
        (constants.FINANCE, 'UK Export Finance (UKEF)'),
        (constants.EUEXIT, 'EU exit enquiries'),  # possibly removed by mixin
        (constants.EVENTS, 'Events'),
        (constants.DSO, 'Defence and Security Organisation (DSO)'),
        (constants.OTHER, 'Other'),
    )
    choice = fields.ChoiceField(
        label='',
        widget=widgets.RadioSelect(),
        choices=CHOICES,  # possibly update by mixin
    )


class GreatServicesRoutingForm(forms.Form):

    CHOICES = (
        (constants.EXPORT_OPPORTUNITIES, 'Export opportunities service'),
        (constants.GREAT_ACCOUNT, 'Your account on great.gov.uk'),
        (constants.OTHER, 'Other'),
    )
    choice = fields.ChoiceField(
        label='',
        widget=widgets.RadioSelect(),
        choices=CHOICES,
    )


class ExportOpportunitiesRoutingForm(forms.Form):
    CHOICES = (
        (
            constants.NO_RESPONSE,
            'I haven\'t had a response from the opportunity I applied for'
        ),
        (constants.ALERTS, 'My daily alerts are not relevant to me'),
        (constants.OTHER, 'Other'),
    )
    choice = fields.ChoiceField(
        label='',
        widget=widgets.RadioSelect(),
        choices=CHOICES,
    )


class GreatAccountRoutingForm(NewUserRegOptionFeatureFlagMixin, forms.Form):
    CHOICES = (
        (
            constants.NO_VERIFICATION_EMAIL,
            'I have not received my email confirmation'
        ),
        (constants.PASSWORD_RESET, 'I need to reset my password'),
        (
            constants.COMPANY_NOT_FOUND,  # possibly update by mixin
            'I cannot find my company'
        ),
        (
            constants.COMPANIES_HOUSE_LOGIN,
            'My Companies House login is not working'
        ),
        (
            constants.VERIFICATION_CODE,
            'I do not know where to enter my verification code'
        ),
        (
            constants.NO_VERIFICATION_LETTER,
            'I have not received my letter containing the verification code'
        ),
        (
            constants.NO_VERIFICATION_MISSING,
            'I have not received a verification code'
        ),
        (constants.OTHER, 'Other'),
    )
    choice = fields.ChoiceField(
        label='',
        widget=widgets.RadioSelect(),
        choices=CHOICES,
    )


class InternationalRoutingForm(EuExitOptionFeatureFlagMixin, forms.Form):
    CHOICES = (
        (constants.INVESTING, 'Investing in the UK'),
        (constants.BUYING, 'Find a UK business partner'),
        (constants.EUEXIT, 'EU exit enquiries'),  # possibly removed by mixin
        (constants.OTHER, 'Other'),
    )
    choice = fields.ChoiceField(
        label='',
        widget=widgets.RadioSelect(),
        choices=CHOICES,  # possibly updated by mixin
    )


class FeedbackForm(SerializeDataMixin, ZendeskActionMixin, forms.Form):
    name = fields.CharField()
    email = fields.EmailField()
    comment = fields.CharField(
        label='Feedback',
        widget=Textarea,
    )
    captcha = ReCaptchaField(
        label='',
        label_suffix='',
    )
    terms_agreed = fields.BooleanField(
        label=TERMS_LABEL
    )

    @property
    def full_name(self):
        assert self.is_valid()
        return self.cleaned_data['name']


class BaseShortForm(forms.Form):
    comment = fields.CharField(
        label='Please give us as much detail as you can',
        widget=Textarea,
    )
    given_name = fields.CharField(label='First name')
    family_name = fields.CharField(label='Last name')
    email = fields.EmailField()
    company_type = fields.ChoiceField(
        label_suffix='',
        widget=widgets.RadioSelect(),
        choices=COMPANY_TYPE_CHOICES,
    )
    company_type_other = fields.ChoiceField(
        label='Type of organisation',
        label_suffix='',
        choices=(('', 'Please select'),) + COMPANY_TYPE_OTHER_CHOICES,
        required=False,
    )
    organisation_name = fields.CharField()
    postcode = fields.CharField()
    captcha = ReCaptchaField(
        label='',
        label_suffix='',
    )
    terms_agreed = fields.BooleanField(label=TERMS_LABEL)


class ShortNotifyForm(SerializeDataMixin, GovNotifyActionMixin, BaseShortForm):

    @property
    def serialized_data(self):
        data = super().serialized_data
        try:
            details = helpers.retrieve_regional_office(data['postcode'])
        except requests.exceptions.RequestException:
            # post code may be incorrect or a server error may have occurred.
            # Set empty as GovUK notify errors if any variables are missing.
            data['dit_regional_office_name'] = ''
            data['dit_regional_office_email'] = ''
        else:
            data['dit_regional_office_name'] = details['name']
            data['dit_regional_office_email'] = details['email']
        return data


class ShortZendeskForm(SerializeDataMixin, ZendeskActionMixin, BaseShortForm):

    @property
    def full_name(self):
        assert self.is_valid()
        cleaned_data = self.cleaned_data
        return f'{cleaned_data["given_name"]} {cleaned_data["family_name"]}'


class InternationalContactForm(
    SerializeDataMixin, GovNotifyActionMixin, forms.Form
):

    ORGANISATION_TYPE_CHOICES = (
        ('COMPANY', 'Company'),
        ('OTHER', 'Other type of organisation'),
    )

    given_name = fields.CharField()
    family_name = fields.CharField()
    email = fields.EmailField(label='Email address')
    organisation_type = fields.ChoiceField(
        label_suffix='',
        widget=widgets.RadioSelect(),
        choices=ORGANISATION_TYPE_CHOICES
    )
    organisation_name = fields.CharField(label='Your organisation name')
    country_name = fields.ChoiceField(
        choices=[('', 'Please select')] + choices.COUNTRY_CHOICES,
    )
    city = fields.CharField(label='City')
    comment = fields.CharField(
        label='Tell us how we can help',
        widget=Textarea,
    )
    captcha = ReCaptchaField(
        label='',
        label_suffix='',
    )
    terms_agreed = fields.BooleanField(
        label=TERMS_LABEL
    )


class CommentForm(forms.Form):
    comment = fields.CharField(
        label='',
        widget=Textarea,
    )


class PersonalDetailsForm(forms.Form):

    first_name = fields.CharField(label='First name')
    last_name = fields.CharField(label='Last name')
    position = fields.CharField(label='Position in organisation')
    email = fields.EmailField(label='Email address')
    phone = fields.CharField(label='Phone')


class BusinessDetailsForm(forms.Form):
    TURNOVER_OPTIONS = (
        ('', 'Please select'),
        ('0-25k', 'under £25,000'),
        ('25k-100k', '£25,000 - £100,000'),
        ('100k-1m', '£100,000 - £1,000,000'),
        ('1m-5m', '£1,000,000 - £5,000,000'),
        ('5m-25m', '£5,000,000 - £25,000,000'),
        ('25m-50m', '£25,000,000 - £50,000,000'),
        ('50m+', '£50,000,000+')
    )

    company_type = fields.ChoiceField(
        label_suffix='',
        widget=widgets.RadioSelect(),
        choices=COMPANY_TYPE_CHOICES,
    )
    companies_house_number = fields.CharField(
        label='Companies House number',
        required=False,
    )
    company_type_other = fields.ChoiceField(
        label_suffix='',
        choices=(('', 'Please select'),) + COMPANY_TYPE_OTHER_CHOICES,
        required=False,
    )
    organisation_name = fields.CharField()
    postcode = fields.CharField()
    industry = fields.ChoiceField(
        choices=INDUSTRY_CHOICES,
    )
    industry_other = fields.CharField(
        label='Type in your industry',
        widget=TextInput(attrs={'class': 'js-field-other'}),
        required=False,
    )
    turnover = fields.ChoiceField(
        label='Annual turnover (optional)',
        choices=TURNOVER_OPTIONS,
        required=False,
    )
    employees = fields.ChoiceField(
        label='Number of employees (optional)',
        choices=(('', 'Please select'),) + choices.EMPLOYEES,
        required=False,
    )
    captcha = ReCaptchaField(
        label='',
        label_suffix='',
    )
    terms_agreed = fields.BooleanField(
        label=TERMS_LABEL
    )


class SellingOnlineOverseasBusiness(forms.Form):
    company_name = fields.CharField(required=False)
    soletrader = fields.BooleanField(
        label='I don\'t have a company number',
        required=False,
    )
    company_number = fields.CharField(
        label=(
            'The number you received when registering your company at '
            'Companies House.'
        ),
        required=False,
    )
    company_postcode = fields.CharField(
        required=False,  # in js hide if company number is inputted
    )
    website_address = fields.CharField(
        label='Company website',
        help_text='Website address, where we can see your products online.',
        max_length=255,
        required=False,
    )


class SellingOnlineOverseasBusinessDetails(forms.Form):
    TURNOVER_OPTIONS = (
        ('Under 100k', 'Under £100,000'),
        ('100k-500k', '£100,000 to £500,000'),
        ('500k-2m', '£500,001 and £2million'),
        ('2m+', 'More than £2million'),

    )

    turnover = fields.ChoiceField(
        label='Turnover last year',
        help_text=(
            'You may use 12 months rolling or last year\'s annual turnover.'
        ),
        choices=TURNOVER_OPTIONS,
        widget=widgets.RadioSelect(),
    )
    sku_count = IntegerField(
        label='How many stock keeping units (SKUs) do you have?',
        help_text=(
            'A stock keeping unit is an individual item, such as a product '
            'or a service that is offered for sale.'
        )
    )
    trademarked = TypedChoiceField(
        label='Are your products trademarked in your target countries?',
        help_text=(
            'Some marketplaces will only sell products that are trademarked.'
        ),
        label_suffix='',
        coerce=lambda x: x == 'True',
        choices=[(True, 'Yes'), (False, 'No')],
        widget=widgets.RadioSelect(),
        required=False,
    )


class SellingOnlineOverseasExperience(forms.Form):
    EXPERIENCE_OPTIONS = (
        ('Not yet', 'Not yet'),
        ('Yes, sometimes', 'Yes, sometimes'),
        ('Yes, regularly', 'Yes, regularly')
    )

    experience = fields.ChoiceField(
        label='Have you sold products online to customers outside the UK?',
        choices=EXPERIENCE_OPTIONS,
        widget=widgets.RadioSelect(),
    )

    description = fields.CharField(
        label='Pitch your business to this marketplace',
        help_text=(
            'Your pitch is important and the information you provide may be '
            'used to introduce you to the marketplace. You could describe '
            'your business, including your products, your customers and '
            'how you market your products in a few paragraphs.'
        ),
        widget=Textarea,
    )


class SellingOnlineOverseasContactDetails(forms.Form):
    contact_name = fields.CharField()
    contact_email = fields.EmailField(
        label='Email address'
    )
    phone = fields.CharField(label='Telephone number')
    email_pref = fields.BooleanField(
        label='I prefer to be contacted by email',
        required=False,
    )
    captcha = ReCaptchaField(
        label='',
        label_suffix='',
    )
    terms_agreed = fields.BooleanField(
        label=TERMS_LABEL
    )


class OfficeFinderForm(forms.Form):
    MESSAGE_NOT_FOUND = 'The postcode you entered does not exist'

    postcode = fields.CharField(
        label='Enter your postcode',
        help_text='For example SW1A 2AA',
    )

    @cached_property
    def office_details(self):
        try:
            return helpers.retrieve_regional_office(
                self.cleaned_data['postcode']
            )
        except requests.exceptions.RequestException:
            return None

    def clean_postcode(self):
        if not self.office_details:
            raise ValidationError(self.MESSAGE_NOT_FOUND)
        return self.cleaned_data['postcode'].replace(' ', '')


class TradeOfficeContactForm(
    SerializeDataMixin, GovNotifyActionMixin, BaseShortForm
):
    pass
