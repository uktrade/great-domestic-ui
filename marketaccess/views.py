from directory_forms_api_client import actions
from directory_forms_api_client.helpers import Sender

from formtools.wizard.views import NamedUrlSessionWizardView

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.template.loader import render_to_string
from django.template.response import TemplateResponse

from core import mixins
from marketaccess import forms


class MarketAccessView(
    mixins.MarketAccessFeatureFlagMixin,
    TemplateView
):
    template_name = "marketaccess/report_a_barrier.html"


class ReportBarrierEmergencyView(
    mixins.MarketAccessFeatureFlagMixin,
    TemplateView
):
    template_name = "marketaccess/report_barrier_emergency_details.html"


class ReportMarketAccessBarrierSuccessView(
    mixins.MarketAccessFeatureFlagMixin,
    TemplateView
):
    template_name = "marketaccess/report_barrier_form/success.html"


class ReportMarketAccessBarrierFormView(
    mixins.MarketAccessFeatureFlagMixin,
    NamedUrlSessionWizardView
):
    CURRENT_STATUS = 'current-status'
    ABOUT = 'about'
    PROBLEM_DETAILS = 'problem-details'
    OTHER_DETAILS = 'other-details'
    SUMMARY = 'summary'
    FINISHED = 'finished'

    form_list = (
        (CURRENT_STATUS, forms.CurrentStatusForm),
        (ABOUT, forms.AboutForm),
        (PROBLEM_DETAILS, forms.ProblemDetailsForm),
        (OTHER_DETAILS, forms.OtherDetailsForm),
        (SUMMARY, forms.SummaryForm),
    )

    form_template_directory = 'marketaccess/report_barrier_form/'
    templates = {
        CURRENT_STATUS: f'{form_template_directory}step-current-status.html',
        ABOUT: f'{form_template_directory}step-about.html',
        PROBLEM_DETAILS: f'{form_template_directory}step-problem.html',
        OTHER_DETAILS: f'{form_template_directory}step-others.html',
        SUMMARY: f'{form_template_directory}step-summary.html',
        FINISHED: f'{form_template_directory}success.html',
    }

    def get_template_names(self):
        return [self.templates[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        if self.steps.current == self.SUMMARY:
            data = self.get_all_cleaned_data()
            context['all_cleaned_data'] = data
        if form.errors:
            for field in form:
                context['formatted_form_errors'] = render_to_string(
                    'marketaccess/report_barrier_form/error-link-list.html',
                    {'form': form}
                )
        return context

    def render_next_step(self, form, **kwargs):
        """
        When using the NamedUrlWizardView, we have to redirect to update the
        browser's URL to match the shown step.
        """
        status = self.get_cleaned_data_for_step(self.CURRENT_STATUS)['status']
        if self.steps.current == self.CURRENT_STATUS and status != "4":
            return redirect('market-access-emergency')
        else:
            return super().render_next_step(form=form, **kwargs)

    def serialize_form_list(self, form_list):
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)
        return data

    def done(self, form_list, form_dict, **kwargs):
        data = self.serialize_form_list(form_list)
        subject = (
            f"{settings.MARKET_ACCESS_ZENDESK_SUBJECT}: "
            f"{data['country']}: "
            f"{data['company_name']}"
        )
        sender = Sender(email_address=data['email'], country_code=None)
        action = actions.ZendeskAction(
            email_address=data['email'],
            full_name=f"{data['firstname']} {data['lastname']}",
            subject=subject,
            service_name=settings.MARKET_ACCESS_FORMS_API_ZENDESK_SEVICE_NAME,
            form_url=reverse(
                'report-ma-barrier', kwargs={'step': 'about'}
            ),
            sender=sender,
        )
        response = action.save(data)
        response.raise_for_status()

        context = {'all_cleaned_data': self.get_all_cleaned_data()}
        return TemplateResponse(
            self.request,
            self.templates['finished'],
            context
        )
