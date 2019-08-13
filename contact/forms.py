from captcha.fields import ReCaptchaField
from directory_components import forms
from directory_constants import choices, urls
from directory_forms_api_client.forms import (
    GovNotifyActionMixin, ZendeskActionMixin
)
import requests.exceptions

from django.conf import settings
from django.forms import Textarea, TextInput, TypedChoiceField
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


class ExportingToUKOptionFeatureFlagMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not settings.FEATURE_FLAGS['EXPORTING_TO_UK_ON']:
            self.fields['choice'].choices = [
                (value, label) for value, label in self.CHOICES
                if value != constants.EXPORTING_TO_UK
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
    choice = forms.ChoiceField(
        label='',
        widget=forms.RadioSelect(),
        choices=CHOICES,
    )


class DomesticRoutingForm(forms.Form):

    CHOICES = (
        (constants.TRADE_OFFICE, 'Find your local trade office'),
        (constants.EXPORT_ADVICE, 'Advice to export from the UK'),
        (
            constants.GREAT_SERVICES,
            'great.gov.uk account and services support'
        ),
        (constants.FINANCE, 'UK Export Finance (UKEF)'),
        (constants.EUEXIT, 'Brexit enquiries'),  # possibly removed by mixin
        (constants.EVENTS, 'Events'),
        (constants.DSO, 'Defence and Security Organisation (DSO)'),
        (constants.OTHER, 'Other'),
    )
    choice = forms.ChoiceField(
        label='',
        widget=forms.RadioSelect(),
        choices=CHOICES,  # possibly update by mixin
    )


class GreatServicesRoutingForm(forms.Form):

    CHOICES = (
        (constants.EXPORT_OPPORTUNITIES, 'Export opportunities service'),
        (constants.GREAT_ACCOUNT, 'Your account on great.gov.uk'),
        (constants.OTHER, 'Other'),
    )
    choice = forms.ChoiceField(
        label='',
        widget=forms.RadioSelect(),
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
    choice = forms.ChoiceField(
        label='',
        widget=forms.RadioSelect(),
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
    choice = forms.ChoiceField(
        label='',
        widget=forms.RadioSelect(),
        choices=CHOICES,
    )


class InternationalRoutingForm(
    ExportingToUKOptionFeatureFlagMixin, forms.Form
):
    CHOICES = (
        (constants.INVESTING, 'Investing in the UK'),
        (constants.CAPITAL_INVEST, 'Capital Investment in the UK'),
        (constants.EXPORTING_TO_UK, 'Exporting to the UK'),
        (constants.BUYING, 'Find a UK business partner'),
        (constants.EUEXIT, 'Brexit enquiries'),  # possibly removed by mixin
        (constants.OTHER, 'Other'),
    )
    choice = forms.ChoiceField(
        label='',
        widget=forms.RadioSelect(),
        choices=CHOICES,  # possibly updated by mixin
    )


class ExportingIntoUKRoutingForm(forms.Form):
    CHOICES = (
        (
            constants.HMRC,
            mark_safe(
                '<p>Commodity codes, taxes, tariffs and other measures, '
                'import procedures</p>'
                '<p class="form-hint">Your question will be sent to Her '
                'Majesty\'s Revenue and Customs (HMRC) to review and '
                'answer</a>'
            ),
        ),
        (
            constants.DEFRA,
            mark_safe(
                '<p>Bringing animals, plants or food into the UK, '
                'environmental regulations, sanitary and phytosanitary '
                'regulations</p>'
                '<p class="form-hint">Your question will be sent to the '
                'Department for Environment, Food and Rural Affairs (Defra) '
                'to review and answer</p>'
            )
        ),
        (
            constants.BEIS,
            mark_safe(
                '<p>Product safety and standards, packaging and labelling</p>'
                '<p class="form-hint">Your question will be sent to the '
                'department for Business, Energy and Industrial Strategy '
                '(BEIS) to review and answer</p>'
            )
        ),
        (
            constants.IMPORT_CONTROLS,
            'Import controls, trade agreements, rules of origin'
        ),
        (
            constants.TRADE_WITH_UK_APP,
            (
                'Help using the ‘Trade with the UK: look up tariffs, taxes '
                'and rules’ service.'
            )
        ),
        (constants.OTHER, 'Other'),
    )
    choice = forms.ChoiceField(
        label='',
        widget=forms.RadioSelect(),
        choices=CHOICES,
    )


class FeedbackForm(SerializeDataMixin, ZendeskActionMixin, forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    comment = forms.CharField(
        label='Feedback',
        widget=Textarea,
    )
    captcha = ReCaptchaField(label_suffix='')
    terms_agreed = forms.BooleanField(
        label=TERMS_LABEL
    )

    @property
    def full_name(self):
        assert self.is_valid()
        return self.cleaned_data['name']


class BaseShortForm(forms.Form):
    comment = forms.CharField(
        label='Please give us as much detail as you can',
        widget=Textarea,
    )
    given_name = forms.CharField(label='First name')
    family_name = forms.CharField(label='Last name')
    email = forms.EmailField()
    company_type = forms.ChoiceField(
        label='Company type',
        label_suffix='',
        widget=forms.RadioSelect(),
        choices=COMPANY_TYPE_CHOICES,
    )
    company_type_other = forms.ChoiceField(
        label='Type of organisation',
        label_suffix='',
        choices=(('', 'Please select'),) + COMPANY_TYPE_OTHER_CHOICES,
        required=False,
    )
    organisation_name = forms.CharField()
    postcode = forms.CharField()
    captcha = ReCaptchaField(label_suffix='')
    terms_agreed = forms.BooleanField(label=TERMS_LABEL)


class ShortNotifyForm(SerializeDataMixin, GovNotifyActionMixin, BaseShortForm):

    @property
    def serialized_data(self):
        data = super().serialized_data
        try:
            details = helpers.retrieve_regional_office(data['postcode'])
        except requests.exceptions.RequestException:
            pass
        else:
            if details:
                data['dit_regional_office_name'] = details['name']
                data['dit_regional_office_email'] = details['email']
        data.setdefault('dit_regional_office_name', '')
        data.setdefault('dit_regional_office_email', '')
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

    given_name = forms.CharField()
    family_name = forms.CharField()
    email = forms.EmailField(label='Email address')
    organisation_type = forms.ChoiceField(
        label_suffix='',
        widget=forms.RadioSelect(),
        choices=ORGANISATION_TYPE_CHOICES
    )
    organisation_name = forms.CharField(label='Your organisation name')
    country_name = forms.ChoiceField(
        choices=[('', 'Please select')] + choices.COUNTRY_CHOICES,
    )
    city = forms.CharField(label='City')
    comment = forms.CharField(
        label='Tell us how we can help',
        help_text=(
            'Do not include personal information or anything of a '
            'sensitive nature'
        ),
        widget=Textarea,
    )
    captcha = ReCaptchaField(label_suffix='')
    terms_agreed = forms.BooleanField(
        label=TERMS_LABEL
    )


class CommentForm(forms.Form):
    comment = forms.CharField(
        label='',
        widget=Textarea,
    )


class PersonalDetailsForm(forms.Form):

    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Last name')
    position = forms.CharField(label='Position in organisation')
    email = forms.EmailField(label='Email address')
    phone = forms.CharField(label='Phone')


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

    company_type = forms.ChoiceField(
        label_suffix='',
        widget=forms.RadioSelect(),
        choices=COMPANY_TYPE_CHOICES,
    )
    companies_house_number = forms.CharField(
        label='Companies House number',
        required=False,
    )
    company_type_other = forms.ChoiceField(
        label_suffix='',
        choices=(('', 'Please select'),) + COMPANY_TYPE_OTHER_CHOICES,
        required=False,
    )
    organisation_name = forms.CharField()
    postcode = forms.CharField()
    industry = forms.ChoiceField(
        choices=INDUSTRY_CHOICES,
    )
    industry_other = forms.CharField(
        label='Type in your industry',
        widget=TextInput(attrs={'class': 'js-field-other'}),
        required=False,
    )
    turnover = forms.ChoiceField(
        label='Annual turnover (optional)',
        choices=TURNOVER_OPTIONS,
        required=False,
    )
    employees = forms.ChoiceField(
        label='Number of employees (optional)',
        choices=(('', 'Please select'),) + choices.EMPLOYEES,
        required=False,
    )
    captcha = ReCaptchaField(label_suffix='')
    terms_agreed = forms.BooleanField(
        label=TERMS_LABEL
    )


class SellingOnlineOverseasBusiness(forms.Form):
    company_name = forms.CharField(required=True)
    soletrader = forms.BooleanField(
        label='I don\'t have a company number',
        required=False,
    )
    company_number = forms.CharField(
        label='Companies House Number',
        help_text=(
            'The number you received when '
            'registering your company at Companies House.'
        ),
        required=False,  # Only need if soletrader false - see clean (below)
    )
    company_postcode = forms.CharField(
        required=True,
    )
    website_address = forms.CharField(
        label='Company website',
        help_text='Website address, where we can see your products online.',
        max_length=255,
        required=True,
    )

    def clean(self):
        cleaned_data = super().clean()
        soletrader = cleaned_data.get('soletrader')
        company_number = cleaned_data.get('company_number')
        if not soletrader and not company_number:
            self.add_error('company_number',
                           self.fields['company_number']
                           .error_messages['required'])


class SellingOnlineOverseasBusinessDetails(forms.Form):
    TURNOVER_OPTIONS = (
        ('Under 100k', 'Under £100,000'),
        ('100k-500k', '£100,000 to £500,000'),
        ('500k-2m', '£500,001 and £2million'),
        ('2m+', 'More than £2million'),

    )

    turnover = forms.ChoiceField(
        label='Turnover last year',
        help_text=(
            'You may use 12 months rolling or last year\'s annual turnover.'
        ),
        choices=TURNOVER_OPTIONS,
        widget=forms.RadioSelect(),
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
        widget=forms.RadioSelect(),
        required=False,
    )


class SellingOnlineOverseasExperience(forms.Form):
    EXPERIENCE_OPTIONS = (
        ('Not yet', 'Not yet'),
        ('Yes, sometimes', 'Yes, sometimes'),
        ('Yes, regularly', 'Yes, regularly')
    )

    experience = forms.ChoiceField(
        label='Have you sold products online to customers outside the UK?',
        choices=EXPERIENCE_OPTIONS,
        widget=forms.RadioSelect(),
    )

    description = forms.CharField(
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
    contact_name = forms.CharField()
    contact_email = forms.EmailField(
        label='Email address'
    )
    phone = forms.CharField(label='Telephone number')
    email_pref = forms.BooleanField(
        label='I prefer to be contacted by email',
        required=False,
    )
    captcha = ReCaptchaField(label_suffix='')
    terms_agreed = forms.BooleanField(
        label=TERMS_LABEL
    )


class OfficeFinderForm(forms.Form):
    MESSAGE_NOT_FOUND = 'The postcode you entered does not exist'

    postcode = forms.CharField(
        label='Enter your postcode',
        help_text='For example SW1A 2AA',
    )

    def clean_postcode(self):
        return self.cleaned_data['postcode'].replace(' ', '')


class TradeOfficeContactForm(
    SerializeDataMixin, GovNotifyActionMixin, BaseShortForm
):
    pass
