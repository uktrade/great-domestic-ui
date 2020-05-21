from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from marketing import forms
from core.views import BaseNotifyFormView
from core.helpers import NotifySettings
from core.helpers import retrieve_regional_office_email


class MarketingJoinFormPageView(BaseNotifyFormView):
    template_name = 'marketing/join-form.html'
    form_class = forms.MarketingJoinForm
    success_url = reverse_lazy('marketing-join-success')

    @staticmethod
    def get_agent_email(postcode):
        region_email = retrieve_regional_office_email(postcode=postcode)
        return region_email or settings.COMMUNITY_ENQUIRIES_AGENT_EMAIL_ADDRESS

    def form_valid(self, form):
        self.notify_settings = NotifySettings(
            agent_template=settings.COMMUNITY_ENQUIRIES_AGENT_NOTIFY_TEMPLATE_ID,
            agent_email=self.get_agent_email(form.cleaned_data['company_postcode']),
            user_template=settings.COMMUNITY_ENQUIRIES_USER_NOTIFY_TEMPLATE_ID,
        )
        return super().form_valid(form)


class MarketingSuccessPageView(TemplateView):
    template_name = 'marketing/join-success.html'
