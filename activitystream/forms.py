from directory_forms_api_client import forms

class FeedbackForm(forms.ZendeskAPIForm):
    result_found fields.BooleanField()
    search_target = fields.CharField()
    reason_for_site_visit = fields.CharField()
    from_search_query = fields.CharField(widget=forms.HiddenInput())
    from_search_page = fields.IntegerField(widget=forms.HiddenInput())
