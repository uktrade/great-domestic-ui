from django.forms import HiddenInput, Textarea, IntegerField

from captcha.fields import ReCaptchaField
from directory_components import forms
from directory_forms_api_client.forms import ZendeskAPIForm


class FeedbackForm(ZendeskAPIForm):
    result_found = forms.ChoiceField(
        label='Did you find what you were looking for?',
        widget=forms.RadioSelect(),
        choices=[
          ('yes', 'Yes'),
          ('no', 'No')
        ]
    )
    search_target = forms.CharField(
       label='What were you looking to find?',
       widget=Textarea(
         attrs={'rows': 4, 'cols': 15}
       )
    )
    reason_for_site_visit = forms.CharField(
        label='Why did you visit this site today?',
        widget=Textarea(
          attrs={'rows': 4, 'cols': 15}
        ))
    from_search_query = forms.CharField(widget=HiddenInput, required=False)
    from_search_page = IntegerField(widget=HiddenInput, required=False)
    contactable = forms.ChoiceField(
        label=('May we contact you with'
               ' follow-up questions about your experience?'),
        widget=forms.RadioSelect(),
        choices=[
          ('yes', 'Yes'),
          ('no', 'No')
        ]
    )
    contact_name = forms.CharField(
        label='What is your name?',
        required=False
    )
    contact_email = forms.EmailField(
        label='What is your email address?',
        required=False
    )
    contact_number = forms.CharField(
        label='What is your phone number? (optional)',
        required=False
    )
    captcha = ReCaptchaField(
        label_suffix='',
        error_messages={
            'required': ('Check the box to confirm that you’re human')
        }
    )
