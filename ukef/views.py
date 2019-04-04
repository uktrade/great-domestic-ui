from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from article.views import CMSPageView
from core.helpers import NotifySettings
from core.views import BaseNotifyFormView
from ukef.forms import UKEFContactForm


class UKEFHomeView(CMSPageView):
    template_name = 'ukef/home_page.html'


class UKEFLandingView(CMSPageView):
    template_name = 'ukef/landing_page.html'


class UKEFContactView(BaseNotifyFormView):
    template_name = 'ukef/contact_form.html'
    form_class = UKEFContactForm
    success_url = reverse_lazy('uk-export-contract-success')
    notify_settings = NotifySettings(
        agent_template=settings.UKEF_CONTACT_AGENT_NOTIFY_TEMPLATE_ID,
        agent_email=settings.UKEF_CONTACT_AGENT_EMAIL_ADDRESS,
        user_template=settings.UKEF_CONTACT_USER_NOTIFY_TEMPLATE_ID,
    )


class UKEFSuccessPageView(TemplateView):
    template_name = 'ukef/contact_form_success.html'

