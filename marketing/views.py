from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from community import forms
from core.views import BaseNotifyFormView
from core.helpers import NotifySettings


class MarketingJoinFormPageView(BaseNotifyFormView):
    template_name = 'community/join-form.html'
    form_class = forms.CommunityJoinForm
    success_url = reverse_lazy('community-join-success')
    notify_settings = NotifySettings(
        agent_template=settings.COMMUNITY_ENQUIRIES_AGENT_NOTIFY_TEMPLATE_ID,
        agent_email=settings.COMMUNITY_ENQUIRIES_AGENT_EMAIL_ADDRESS,
        user_template=settings.COMMUNITY_ENQUIRIES_USER_NOTIFY_TEMPLATE_ID,
    )


class CommunitySuccessPageView(TemplateView):
    template_name = 'community/join-success.html'
