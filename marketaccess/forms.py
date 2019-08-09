from directory_components import forms
from django.utils.safestring import mark_safe

from django.forms import Textarea, TextInput


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

    location = forms.CharField(
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
                'Tell us what you’ve done to resolve your ',
                'problem, even if this is your first step'
            )
        }
    )
    eu_exit_related = forms.ChoiceField(
        label='Is your problem caused by or related to Brexit?',
        widget=forms.RadioSelect(
            use_nice_ids=True, attrs={'id': 'radio-one'}
        ),
        choices=(
            ('Yes', 'Yes'),
            ('No', 'No')
        ),
        error_messages={
            'required': 'Tell us if your problem is related to Brexit'
        }
    )


class SummaryForm(forms.Form):
    pass
