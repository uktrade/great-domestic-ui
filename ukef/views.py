from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from core.helpers import NotifySettings
from core.views import BaseNotifyFormView
from ukef.forms import UKEFContactForm
from ukef.mixins import UKEFPagesFeatureFlagMixin


class HomeView(UKEFPagesFeatureFlagMixin, TemplateView):
    template_name = 'ukef/home_page.html'


class LandingView(UKEFPagesFeatureFlagMixin, TemplateView):
    template_name = 'ukef/landing_page.html'


class ContactView(UKEFPagesFeatureFlagMixin, BaseNotifyFormView):
    template_name = 'ukef/contact_form.html'
    form_class = UKEFContactForm
    success_url = reverse_lazy('uk-export-contract-success')
    notify_settings = NotifySettings(
        agent_template=settings.UKEF_CONTACT_AGENT_NOTIFY_TEMPLATE_ID,
        agent_email=settings.UKEF_CONTACT_AGENT_EMAIL_ADDRESS,
        user_template=settings.UKEF_CONTACT_USER_NOTIFY_TEMPLATE_ID,
    )

    def form_valid(self, form):
        user_email = form.cleaned_data['email']
        self.request.session['user_email'] = user_email
        return super().form_valid(form)


class SuccessPageView(UKEFPagesFeatureFlagMixin, TemplateView):
    template_name = 'ukef/contact_form_success.html'

    def get(self, *args, **kwargs):
        if not self.request.session.get('user_email'):
            return HttpResponseRedirect(reverse_lazy('uk-export-contact'))
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['user_email'] = self.request.session.get('user_email')
        return super().get_context_data(**kwargs)


class HowWeAssessPageView(UKEFPagesFeatureFlagMixin, TemplateView):
    template_name = 'ukef/how_we_assess.html'


class WhatWeOfferView(UKEFPagesFeatureFlagMixin, TemplateView):
    template_name = 'ukef/what_we_offer.html'


class CountryCoverView(UKEFPagesFeatureFlagMixin, TemplateView):
    template_name = 'ukef/country_cover.html'
