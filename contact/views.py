from directory_constants.constants import urls
from formtools.wizard.views import SessionWizardView
from formtools.wizard.views import NamedUrlSessionWizardView
from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.edit import FormView

from contact import forms


class FeatureFlagMixin:
    def dispatch(self, *args, **kwargs):
        if not settings.FEATURE_FLAGS['CONTACT_US_ON']:
            raise Http404()
        return super().dispatch(*args, **kwargs)


class RoutingFormView(FeatureFlagMixin, NamedUrlSessionWizardView):
    LOCATION = 'location'
    INTERNATIONAL = 'international'
    DOMESTIC = 'domestic'
    GREAT_SERVICES = 'great-services'
    GREAT_ACCOUNT = 'great-account'
    EXPORT_OPPORTUNITIES = 'export-opportunities'

    form_list = (
        (LOCATION, forms.LocationRoutingForm),
        (DOMESTIC, forms.DomesticRoutingForm),
        (GREAT_SERVICES, forms.GreatServicesRoutingForm),
        (GREAT_ACCOUNT, forms.GreatAccountRoutingForm),
        (EXPORT_OPPORTUNITIES, forms.ExportOpportunitiesServiceRoutingForm),
        (INTERNATIONAL, forms.InternationalRoutingForm),
        ('BLANK', forms.InternationalRoutingForm), # should never be reached
    )
    templates = {
        LOCATION: 'contact/routing/step-location.html',
        DOMESTIC: 'contact/routing/step-domestic.html',
        GREAT_SERVICES: 'contact/routing/step-great-services.html',
        GREAT_ACCOUNT: 'contact/routing/step-great-account.html',
        EXPORT_OPPORTUNITIES: 'contact/routing/step-export-opportunities-service.html',
        INTERNATIONAL: 'contact/routing/step-international.html',
    }

    def get_template_names(self):
        return [self.templates[self.steps.current]]

    def done(self, *args, **kwargs):
        #  ¯\_(ツ)_/¯
        pass

    def render_next_step(self, form):
        choice = form.cleaned_data['choice']
        if self.steps.current == self.DOMESTIC:
            if choice == form.EXPORT_ADVICE:
                return redirect(reverse('contact-us-export-advice'))
            elif choice == form.FINANCE:
                return redirect(reverse('contact-us-finance-form'))
            elif choice == form.EVENTS:
                return redirect(urls.SERVICES_EVENTS)
            elif choice == form.DSO:
                return redirect(reverse('contact-us-domestic'))
            elif choice == form.OTHER:
                return redirect(reverse('contact-us-domestic'))
        elif self.steps.current == self.INTERNATIONAL:
            if choice == form.INVESTING:
                return redirect(settings.INVEST_CONTACT_URL)
            elif choice == form.BUYING:
                return redirect(reverse('contact-us-find-uk-companies'))
            elif choice == form.EUEXIT:
                return redirect(reverse('eu-exit-international-contact-form'))
            elif choice == form.OTHER:
                return redirect(reverse('contact-us-international'))
        return self.render_goto_step(choice)



class FinanceFormView(FeatureFlagMixin, SessionWizardView):
    SELECT = 'select'
    PERSONAL = 'personal-details'
    BUSINESS = 'business-details'

    form_list = (
        (SELECT, forms.FinanceInfomationChoicesForm),
        (PERSONAL, forms.FinancePersonalDetailsForm),
        (BUSINESS, forms.FinanceBusinessDetailsForm),
    )
    templates = {
        SELECT: 'contact/finance/step-select.html',
        PERSONAL: 'contact/finance/step-personal.html',
        BUSINESS: 'contact/finance/step-business.html',
    }

    def get_template_names(self):
        return [self.templates[self.steps.current]]

    def done(self, *args, **kwargs):
        #  ¯\_(ツ)_/¯
        pass


class ExportAdviceFormView(FeatureFlagMixin, FormView):
    form_class = forms.ExportAdviceContactForm
    template_name = 'contact/export-advice/step.html'


class BuyingFromUKCompaniesFormView(FeatureFlagMixin, FormView):
    form_class = forms.BuyingFromUKContactForm
    template_name = 'contact/buying/step.html'


class InternationalFormView(FeatureFlagMixin, FormView):
    form_class = forms.InternationalContactForm
    template_name = 'contact/international/step.html'


class DomesticFormView(FeatureFlagMixin, FormView):
    form_class = forms.DomesticContactForm
    template_name = 'contact/domestic/step.html'
