from directory_components import forms
from directory_constants import choices
from django.utils.safestring import mark_safe

from django.forms import Textarea, TextInput

from marketaccess import widgets


LOCATION_CHOICES = [('', 'Please select')] + choices.COUNTRIES_AND_TERRITORIES
LOCATION_MAP = dict(LOCATION_CHOICES)
PROBLEM_CAUSE_CHOICES = (
    ('brexit', 'Brexit'),
    ('covid-19', 'Covid-19'),
)
PROBLEM_CAUSE_MAP = dict(PROBLEM_CAUSE_CHOICES)


class AboutForm(forms.Form):
    error_css_class = 'input-field-container has-error'
    CATEGORY_CHOICES = (
        'I’m an exporter or investor, or I want to export or invest',
        'I work for a trade association',
        'Other'
    )

    firstname = forms.CharField(
        label='First name',
        error_messages={
            'required': 'Enter your first name'
        }
    )

    lastname = forms.CharField(
        label='Last name',
        error_messages={
            'required': 'Enter your last name'
        }
    )

    jobtitle = forms.CharField(
        label='Job title',
        error_messages={
            'required': 'Enter your job title'
        }
    )

    business_type = forms.ChoiceField(
        label='Business type',
        widget=forms.RadioSelect(
            attrs={'id': 'checkbox-single'},
            use_nice_ids=True,
        ),
        choices=((choice, choice) for choice in CATEGORY_CHOICES),
        error_messages={
            'required': 'Tell us your business type'
        }
    )
    other_business_type = forms.CharField(
        label='Tell us about your organisation',
        widget=TextInput(attrs={'class': 'js-field-other'}),
        required=False
    )

    company_name = forms.CharField(
        label='Business or organisation name',
        error_messages={
            'required': 'Enter your business or organisation name'
        }
    )

    email = forms.EmailField(
        label='Email address',
        error_messages={
            'required': 'Enter your email address'
        }
    )

    phone = forms.CharField(
        label='Telephone number',
        error_messages={
            'required': 'Enter your telephone number'
        }
    )

    def clean(self):
        data = self.cleaned_data
        other_business_type = data.get('other_business_type')
        business_type = data.get('business_type')
        if business_type == 'Other' and not other_business_type:
            self.add_error(
                'other_business_type', 'Enter your organisation'
            )
        else:
            return data


class ProblemDetailsForm(forms.Form):

    error_css_class = 'input-field-container has-error'

    location = forms.ChoiceField(
        choices=LOCATION_CHOICES,
        label='Where are you trying to export to or invest in?',
        error_messages={
            'required': (
                'Tell us where you are trying to export to or invest in'
            )
        }
    )
    product_service = forms.CharField(
        label='What goods or services do you want to export?',
        help_text='Or tell us about an investment you want to make',
        error_messages={
            'required': (
                'Tell us what you’re trying to export or invest in'
            )
        }
    )
    problem_summary = forms.CharField(
        label=mark_safe(
            (
                '<p>Tell us about your problem, including: </p>'
                '<ul class="list list-bullet">'
                '<li>what’s affecting your export or investment</li>'
                '<li>when you became aware of the problem</li>'
                '<li>how you became aware of the problem</li>'
                '<li>if this has happened before</li>'
                '<li>'
                'any information you’ve been given or '
                'correspondence you’ve had'
                '</li>'
                '<li>'
                'the HS (Harmonized System) code for your goods, '
                'if you know it'
                '</li>'
                '<li>'
                'if it is an existing barrier include the trade '
                'barrier code and title (to find the title and '
                'code visit '
                '<a href="https://www.gov.uk/barriers-trading-investing-abroad" target="_blank" class="link">'
                'check for barriers to trading and investing abroad</a>.)'
                '</li>'
                '</ul>'
            )
        ),
        widget=Textarea,
        error_messages={
            'required': 'Tell us about the problem you’re facing'
        }
    )
    impact = forms.CharField(
        label=(
            'How has the problem affected your business or '
            'industry, or how could it affect it?'
        ),
        widget=Textarea,
        error_messages={
            'required': (
                'Tell us how your business or industry '
                'is being affected by the problem'
            )
        }
    )
    resolve_summary = forms.CharField(
        label=mark_safe(
            (
                '<p>Tell us about any steps you’ve taken '
                'to resolve the problem, including: </p>'
                '<ul class="list list-bullet">'
                '<li>people you’ve contacted</li>'
                '<li>when you contacted them</li>'
                '<li>what happened</li>'
                '</ul>'
            )
        ),
        widget=Textarea,
        error_messages={
            'required': (
                'Tell us what you’ve done to resolve your '
                'problem, even if this is your first step'
            )
        }
    )
    problem_cause = forms.MultipleChoiceField(
        label='Is the problem caused by or related to any of the following?',
        widget=widgets.TickboxWithOptionsHelpText(
            use_nice_ids=True,
            attrs={
                'id': 'radio-one',
                'help_text': {
                     'radio-one-covid-19': 'Problem related to the COVID-19 (coronavirus) pandemic.',
                }
            },
        ),
        choices=PROBLEM_CAUSE_CHOICES,
        required=False,
    )

    def clean_location(self):
        value = self.cleaned_data['location']
        self.cleaned_data['location_label'] = LOCATION_MAP[value]
        return value

    def clean_problem_cause(self):
        value = self.cleaned_data['problem_cause']
        self.cleaned_data['problem_cause_label'] = [PROBLEM_CAUSE_MAP[item] for item in value]
        return value


class SummaryForm(forms.Form):
    contact_by_email = forms.BooleanField(
        label='I would like to receive additional information by email',
        required=False,
    )
    contact_by_phone = forms.BooleanField(
        label='I would like to receive additional information by telephone',
        required=False,
    )
