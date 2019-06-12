from django.forms import HiddenInput, Textarea, IntegerField

from directory_components import fields, widgets
from directory_forms_api_client import forms


class FeedbackForm(forms.ZendeskAPIForm):
    result_found = fields.ChoiceField(
      label='Did you find what you were looking for?',
      widget=widgets.RadioSelect(),
      choices=[
        ('yes', 'Yes'),
        ('no', 'No')
      ],
      required=True)
    search_target = fields.CharField(
      label='What were you looking to find?',
      widget=Textarea(
        attrs={'rows': 4, 'cols': 15}
      ), required=True)
    reason_for_site_visit = fields.CharField(
      label='Why did you visit this site today?',
      widget=Textarea(
        attrs={'rows': 4, 'cols': 15}
      ), required=True)
    from_search_query = fields.CharField(widget=HiddenInput(),
                                         required=False)
    from_search_page = IntegerField(widget=HiddenInput(),
                                    required=False)
    contactable = fields.ChoiceField(
      label='May we contact you with\
 follow-up questions about your experience?',
      widget=widgets.RadioSelect(),
      choices=[
        ('yes', 'Yes'),
        ('no', 'No')
      ],
      required=True
    )
    contact_name = fields.CharField(
      label='What is your name?',
      required=False
    )
    contact_email = fields.EmailField(
      label='What is your email address?',
      required=False
    )
    contact_number = fields.CharField(
      label='What is your phone number? (optional)',
      required=False
    )
