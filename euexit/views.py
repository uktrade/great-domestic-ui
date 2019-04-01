from directory_components.mixins import CountryDisplayMixin
from directory_constants.constants import cms
from directory_forms_api_client.helpers import Sender

from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from core.mixins import GetCMSPageMixin, PrepopulateFormMixin
from euexit import forms, mixins


SESSION_KEY_FORM_INGRESS_URL = 'FORM_INGRESS_URL'


class BaseInternationalContactFormView(
    mixins.EUExitFormsFeatureFlagMixin,
    GetCMSPageMixin,
    PrepopulateFormMixin,
    mixins.HideLanguageSelectorMixin,
    CountryDisplayMixin,
    FormView,
):

    def get(self, *args, **kwargs):
        self.request.session[SESSION_KEY_FORM_INGRESS_URL] = (
            self.request.META.get('HTTP_REFERER')
        )
        return super().get(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['field_attributes'] = self.page
        kwargs['ingress_url'] = (
            self.request.session.get(SESSION_KEY_FORM_INGRESS_URL)
        )
        kwargs['disclaimer'] = self.page['disclaimer']
        return kwargs

    def form_valid(self, form):
        sender = Sender(
            email_address=form.cleaned_data['email'],
            country_code=form.cleaned_data.get('country_name'),
        )
        response = form.save(
            subject=self.subject,
            full_name=form.full_name,
            email_address=form.cleaned_data['email'],
            service_name='eu_exit',
            subdomain=settings.EU_EXIT_ZENDESK_SUBDOMAIN,
            form_url=self.request.path,
            sender=sender,
        )
        response.raise_for_status()
        return super().form_valid(form)


class BaseContactView(
    mixins.EUExitFormsFeatureFlagMixin,
    GetCMSPageMixin,
    mixins.HideLanguageSelectorMixin,
    TemplateView
):
    pass


class InternationalContactFormView(BaseInternationalContactFormView):
    slug = cms.GREAT_EUEXIT_INTERNATIONAL_FORM_SLUG
    form_class = forms.InternationalContactForm
    template_name = 'euexit/international-contact-form.html'
    success_url = reverse_lazy('eu-exit-international-contact-form-success')
    subject = 'EU exit international contact form'

    def get_form_initial(self):
        if self.company_profile:
            return {
                'email': self.request.sso_user.email,
                'company_name': self.company_profile['name'],
                'postcode': self.company_profile['postal_code'],
                'first_name': self.guess_given_name,
                'last_name': self.guess_family_name,
                'organisation_type': forms.COMPANY,
                'country': self.company_profile['country'],
                'city': self.company_profile['locality'],
            }


class DomesticContactFormView(BaseInternationalContactFormView):
    slug = cms.GREAT_EUEXIT_DOMESTIC_FORM_SLUG
    form_class = forms.DomesticContactForm
    template_name = 'euexit/domestic-contact-form.html'
    success_url = reverse_lazy('eu-exit-domestic-contact-form-success')
    subject = 'EU exit contact form'

    def get_form_initial(self):
        if self.company_profile:
            return {
                'email': self.request.sso_user.email,
                'company_name': self.company_profile['name'],
                'postcode': self.company_profile['postal_code'],
                'first_name': self.guess_given_name,
                'last_name': self.guess_family_name,
                'organisation_type': forms.COMPANY,
            }


class InternationalContactSuccessView(BaseContactView):
    template_name = 'euexit/international-contact-form-success.html'
    slug = cms.GREAT_EUEXIT_FORM_SUCCESS_SLUG


class DomesticContactSuccessView(BaseContactView):
    template_name = 'euexit/domestic-contact-form-success.html'
    slug = cms.GREAT_EUEXIT_FORM_SUCCESS_SLUG
