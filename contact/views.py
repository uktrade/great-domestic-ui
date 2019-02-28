from urllib.parse import urlparse

from directory_constants.constants import cms
from directory_forms_api_client import actions
from directory_forms_api_client.helpers import FormSessionMixin, Sender

from formtools.wizard.views import NamedUrlSessionWizardView

from django.conf import settings
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.functional import LazyObject
from django.utils.html import strip_tags
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.template.response import TemplateResponse

from core import mixins
from core.views import BaseNotifyFormView
from core.helpers import NotifySettings
from contact import constants, forms, helpers

SESSION_KEY_SOO_MARKET = 'SESSION_KEY_SOO_MARKET'


class LazyOfficeFinderURL(LazyObject):
    @property
    def _wrapped(self):
        if settings.FEATURE_FLAGS['OFFICE_FINDER_ON']:
            return reverse('office-finder')
        return settings.FIND_TRADE_OFFICE_URL


def build_export_opportunites_guidance_url(step_name, ):
    return reverse_lazy(
        'contact-us-export-opportunities-guidance', kwargs={'slug': step_name}
    )


def build_great_account_guidance_url(step_name, ):
    return reverse_lazy(
        'contact-us-great-account-guidance', kwargs={'slug': step_name}
    )


class SubmitFormOnGetMixin:

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        data = self.request.GET or {}
        if data:
            kwargs['data'] = data
        return kwargs

    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PrepopulateShortFormMixin(mixins.PrepopulateFormMixin):
    def get_form_initial(self):
        if self.company_profile:
            return {
                'email': self.request.sso_user.email,
                'company_type': forms.LIMITED,
                'organisation_name': self.company_profile['name'],
                'postcode': self.company_profile['postal_code'],
                'given_name': self.guess_given_name,
                'family_name': self.guess_family_name,
            }


class BaseZendeskFormView(FormSessionMixin, FormView):

    def form_valid(self, form):
        sender = Sender(
            email_address=form.cleaned_data['email'],
            country_code=None,
        )
        response = form.save(
            email_address=form.cleaned_data['email'],
            full_name=form.full_name,
            subject=self.subject,
            service_name=settings.DIRECTORY_FORMS_API_ZENDESK_SEVICE_NAME,
            form_url=self.request.get_full_path(),
            form_session=self.form_session,
            sender=sender
        )
        response.raise_for_status()
        return super().form_valid(form)


class BaseSuccessView(FormSessionMixin, mixins.GetCMSPageMixin, TemplateView):
    template_name = 'contact/submit-success.html'

    def clear_form_session(self, response):
        self.form_session.clear()

    def get(self, *args, **kwargs):
        # setting ingress url not very meaningful here, so skip it.
        response = super(FormSessionMixin, self).get(*args, **kwargs)
        response.add_post_render_callback(self.clear_form_session)
        return response

    def get_next_url(self):
        # If the ingress URL is internal then allow user to go back to it
        parsed_url = urlparse(self.form_session.ingress_url)
        if parsed_url.netloc == self.request.get_host():
            return self.form_session.ingress_url
        return reverse('landing-page')

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            **kwargs,
            next_url=self.get_next_url()
        )


class RoutingFormView(FormSessionMixin, NamedUrlSessionWizardView):

    # given the current step, based on selected  option, where to redirect.
    redirect_mapping = {
        constants.DOMESTIC: {
            constants.TRADE_OFFICE: LazyOfficeFinderURL(),
            constants.EXPORT_ADVICE: reverse_lazy(
                'contact-us-export-advice',
                kwargs={'step': 'comment'}
            ),
            constants.FINANCE: reverse_lazy(
                'uk-export-finance-lead-generation-form',
                kwargs={'step': 'contact'}
            ),
            constants.EUEXIT: reverse_lazy('eu-exit-domestic-contact-form'),
            constants.EVENTS: reverse_lazy('contact-us-events-form'),
            constants.DSO: reverse_lazy('contact-us-dso-form'),
            constants.OTHER: reverse_lazy('contact-us-enquiries'),
        },
        constants.INTERNATIONAL: {
            constants.INVESTING: settings.INVEST_CONTACT_URL,
            constants.BUYING: settings.FIND_A_SUPPLIER_CONTACT_URL,
            constants.EUEXIT: reverse_lazy(
                'eu-exit-international-contact-form'
            ),
            constants.OTHER: reverse_lazy('contact-us-international'),
        },
        constants.EXPORT_OPPORTUNITIES: {
            constants.NO_RESPONSE: build_export_opportunites_guidance_url(
                cms.GREAT_HELP_EXOPP_NO_RESPONSE
            ),
            constants.ALERTS: build_export_opportunites_guidance_url(
                cms.GREAT_HELP_EXOPP_ALERTS_IRRELEVANT_SLUG
            ),
            constants.OTHER: reverse_lazy('contact-us-domestic'),
        },
        constants.GREAT_SERVICES: {
            constants.OTHER: reverse_lazy('contact-us-domestic'),
        },
        constants.GREAT_ACCOUNT: {
            constants.NO_VERIFICATION_EMAIL: build_great_account_guidance_url(
                cms.GREAT_HELP_MISSING_VERIFY_EMAIL_SLUG
            ),
            constants.PASSWORD_RESET: build_great_account_guidance_url(
                cms.GREAT_HELP_PASSWORD_RESET_SLUG
            ),
            constants.COMPANY_NOT_FOUND: build_great_account_guidance_url(
                cms.GREAT_HELP_ACCOUNT_COMPANY_NOT_FOUND_SLUG
            ),
            constants.SOLE_TRADER_ADDRESS_NOT_FOUND:
                build_great_account_guidance_url(
                cms.GREAT_HELP_ACCOUNT_SOLE_TRADER_ADDRESS_NOT_FOUND_SLUG
            ),
            constants.COMPANIES_HOUSE_LOGIN: build_great_account_guidance_url(
                cms.GREAT_HELP_COMPANIES_HOUSE_LOGIN_SLUG
            ),
            constants.VERIFICATION_CODE: build_great_account_guidance_url(
                cms.GREAT_HELP_VERIFICATION_CODE_ENTER_SLUG,
            ),
            constants.NO_VERIFICATION_LETTER: build_great_account_guidance_url(
                cms.GREAT_HELP_VERIFICATION_CODE_LETTER_SLUG
            ),
            constants.NO_VERIFICATION_MISSING:
                build_great_account_guidance_url(
                cms.GREAT_HELP_VERIFICATION_CODE_MISSING_SLUG
            ),
            constants.OTHER: reverse_lazy('contact-us-domestic'),
        }
    }

    form_list = (
        (constants.LOCATION, forms.LocationRoutingForm),
        (constants.DOMESTIC, forms.DomesticRoutingForm),
        (constants.GREAT_SERVICES, forms.GreatServicesRoutingForm),
        (constants.GREAT_ACCOUNT, forms.GreatAccountRoutingForm),
        (constants.EXPORT_OPPORTUNITIES, forms.ExportOpportunitiesRoutingForm),
        (constants.INTERNATIONAL, forms.InternationalRoutingForm),
        ('NO-OPERATION', forms.NoOpForm),  # should never be reached
    )
    templates = {
        constants.LOCATION: 'contact/routing/step-location.html',
        constants.DOMESTIC: 'contact/routing/step-domestic.html',
        constants.GREAT_SERVICES: 'contact/routing/step-great-services.html',
        constants.GREAT_ACCOUNT: 'contact/routing/step-great-account.html',
        constants.EXPORT_OPPORTUNITIES: (
            'contact/routing/step-export-opportunities-service.html'
        ),
        constants.INTERNATIONAL: 'contact/routing/step-international.html',
    }

    # given current step, where to send them back to
    back_mapping = {
        constants.DOMESTIC: constants.LOCATION,
        constants.INTERNATIONAL: constants.LOCATION,
        constants.GREAT_SERVICES: constants.DOMESTIC,
        constants.GREAT_ACCOUNT: constants.GREAT_SERVICES,
        constants.EXPORT_OPPORTUNITIES: constants.GREAT_SERVICES,
    }

    def get_template_names(self):
        return [self.templates[self.steps.current]]

    def get_redirect_url(self, choice):
        if self.steps.current in self.redirect_mapping:
            mapping = self.redirect_mapping[self.steps.current]
            return mapping.get(choice)

    def render_next_step(self, form):
        self.form_session.funnel_steps.append(self.steps.current)
        choice = form.cleaned_data['choice']
        redirect_url = self.get_redirect_url(choice)
        if redirect_url:
            # clear the ingress URL when redirecting away from the service as
            # the "normal way" for clearing it via success page will not be hit
            # assumed that internal redirects will not contain domain, but be
            # relative to current site.
            if urlparse(str(redirect_url)).netloc:
                self.form_session.clear()
            return redirect(redirect_url)
        return self.render_goto_step(choice)

    def get_prev_step(self, step=None):
        if step is None:
            step = self.steps.current
        return self.back_mapping.get(step)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        parsed_url = urlparse(self.form_session.ingress_url)
        if parsed_url.netloc == self.request.get_host():
            context_data['prev_url'] = self.form_session.ingress_url
        return context_data


class ExportingAdviceFormView(
    mixins.PreventCaptchaRevalidationMixin, FormSessionMixin,
    mixins.PrepopulateFormMixin, NamedUrlSessionWizardView
):
    success_url = reverse_lazy('contact-us-domestic-success')

    COMMENT = 'comment'
    PERSONAL = 'personal'
    BUSINESS = 'business'

    form_list = (
        (COMMENT, forms.CommentForm),
        (PERSONAL, forms.PersonalDetailsForm),
        (BUSINESS, forms.BusinessDetailsForm),
    )

    templates = {
        COMMENT: 'contact/exporting/step-comment.html',
        PERSONAL: 'contact/exporting/step-personal.html',
        BUSINESS: 'contact/exporting/step-business.html',
    }

    def get_template_names(self):
        return [self.templates[self.steps.current]]

    def get_form_kwargs(self, *args, **kwargs):
        # skipping `PrepopulateFormMixin.get_form_kwargs`
        return super(mixins.PrepopulateFormMixin, self).get_form_kwargs(
            *args, **kwargs
        )

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)
        if step == self.PERSONAL and self.company_profile:
            initial.update({
                'email': self.request.sso_user.email,
                'phone': self.company_profile['mobile_number'],
                'first_name': self.guess_given_name,
                'last_name': self.guess_family_name,
            })
        elif step == self.BUSINESS and self.company_profile:
            company = self.company_profile
            initial.update({
                'company_type': forms.LIMITED,
                'companies_house_number': company['number'],
                'organisation_name': company['name'],
                'postcode': company['postal_code'],
                'industry': (
                    company['sectors'][0] if company['sectors'] else None
                ),
                'employees': company['employees'],
            })
        return initial

    def send_user_message(self, form_data):
        action = actions.GovNotifyAction(
            template_id=settings.CONTACT_EXPORTING_USER_NOTIFY_TEMPLATE_ID,
            email_address=form_data['email'],
            form_url=reverse(
                'contact-us-export-advice', kwargs={'step': 'comment'}
            ),
            form_session=self.form_session,
            email_reply_to_id=settings.CONTACT_EXPORTING_USER_REPLY_TO_EMAIL_ID
        )
        response = action.save(form_data)
        response.raise_for_status()

    def send_agent_message(self, form_data):
        sender = Sender(email_address=form_data['email'], country_code=None)
        action = actions.EmailAction(
            recipients=[form_data['region_office_email']],
            subject=settings.CONTACT_EXPORTING_AGENT_SUBJECT,
            reply_to=[settings.DEFAULT_FROM_EMAIL],
            form_url=reverse(
                'contact-us-export-advice', kwargs={'step': 'comment'}
            ),
            form_session=self.form_session,
            sender=sender,
        )
        template_name = 'contact/exporting-from-uk-agent-email.html'
        html = render_to_string(template_name, {'form_data': form_data})
        response = action.save(
            {'text_body': strip_tags(html), 'html_body': html}
        )
        response.raise_for_status()

    def done(self, form_list, **kwargs):
        form_data = self.serialize_form_list(form_list)
        self.send_agent_message(form_data)
        self.send_user_message(form_data)
        return redirect(self.success_url)

    def serialize_form_list(self, form_list):
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)
        del data['terms_agreed']
        data['region_office_email'] = helpers.retrieve_exporting_advice_email(
            data['postcode']
        )
        return data


class FeedbackFormView(mixins.PrepopulateFormMixin, BaseZendeskFormView):
    form_class = forms.FeedbackForm
    template_name = 'contact/comment-contact.html'
    success_url = reverse_lazy('contact-us-feedback-success')
    subject = settings.CONTACT_DOMESTIC_ZENDESK_SUBJECT

    def get_form_initial(self):
        if self.company_profile:
            return {
                'email': self.request.sso_user.email,
                'name': self.company_profile['postal_full_name'],
            }


class DomesticFormView(PrepopulateShortFormMixin, BaseZendeskFormView):
    form_class = forms.ShortZendeskForm
    template_name = 'contact/domestic/step.html'
    success_url = reverse_lazy('contact-us-domestic-success')
    subject = settings.CONTACT_DOMESTIC_ZENDESK_SUBJECT


class DomesticEnquiriesFormView(PrepopulateShortFormMixin, BaseNotifyFormView):
    form_class = forms.ShortNotifyForm
    template_name = 'contact/domestic/step.html'
    success_url = reverse_lazy('contact-us-domestic-success')
    notify_settings = NotifySettings(
        agent_template=settings.CONTACT_ENQUIRIES_AGENT_NOTIFY_TEMPLATE_ID,
        agent_email=settings.CONTACT_ENQUIRIES_AGENT_EMAIL_ADDRESS,
        user_template=settings.CONTACT_ENQUIRIES_USER_NOTIFY_TEMPLATE_ID,
    )


class InternationalFormView(mixins.PrepopulateFormMixin, BaseNotifyFormView):
    form_class = forms.InternationalContactForm
    template_name = 'contact/international/step.html'
    success_url = reverse_lazy('contact-us-international-success')
    notify_settings = NotifySettings(
        agent_template=settings.CONTACT_INTERNATIONAL_AGENT_NOTIFY_TEMPLATE_ID,
        agent_email=settings.CONTACT_INTERNATIONAL_AGENT_EMAIL_ADDRESS,
        user_template=settings.CONTACT_INTERNATIONAL_USER_NOTIFY_TEMPLATE_ID,
    )

    def get_form_initial(self):
        if self.company_profile:
            return {
                'email': self.request.sso_user.email,
                'organisation_name': self.company_profile['name'],
                'country_name': self.company_profile['country'],
                'city': self.company_profile['locality'],
                'given_name': self.guess_given_name,
                'family_name': self.guess_family_name,
            }


class EventsFormView(PrepopulateShortFormMixin, BaseNotifyFormView):
    form_class = forms.ShortNotifyForm
    template_name = 'contact/domestic/step.html'
    success_url = reverse_lazy('contact-us-events-success')
    notify_settings = NotifySettings(
        agent_template=settings.CONTACT_EVENTS_AGENT_NOTIFY_TEMPLATE_ID,
        agent_email=settings.CONTACT_EVENTS_AGENT_EMAIL_ADDRESS,
        user_template=settings.CONTACT_EVENTS_USER_NOTIFY_TEMPLATE_ID,
    )


class DefenceAndSecurityOrganisationFormView(
    PrepopulateShortFormMixin, BaseNotifyFormView
):
    form_class = forms.ShortNotifyForm
    template_name = 'contact/domestic/step.html'
    success_url = reverse_lazy('contact-us-dso-success')
    notify_settings = NotifySettings(
        agent_template=settings.CONTACT_DSO_AGENT_NOTIFY_TEMPLATE_ID,
        agent_email=settings.CONTACT_DSO_AGENT_EMAIL_ADDRESS,
        user_template=settings.CONTACT_DSO_USER_NOTIFY_TEMPLATE_ID,
    )


class InternationalSuccessView(BaseSuccessView):
    slug = cms.GREAT_CONTACT_US_FORM_SUCCESS_INTERNATIONAL_SLUG


class DomesticSuccessView(BaseSuccessView):
    slug = cms.GREAT_CONTACT_US_FORM_SUCCESS_SLUG


class EventsSuccessView(BaseSuccessView):
    slug = cms.GREAT_CONTACT_US_FORM_SUCCESS_EVENTS_SLUG


class DefenceAndSecurityOrganisationSuccessView(BaseSuccessView):
    slug = cms.GREAT_CONTACT_US_FORM_SUCCESS_DSO_SLUG


class ExportingAdviceSuccessView(BaseSuccessView):
    slug = cms.GREAT_CONTACT_US_FORM_SUCCESS_EXPORT_ADVICE_SLUG


class FeedbackSuccessView(BaseSuccessView):
    slug = cms.GREAT_CONTACT_US_FORM_SUCCESS_FEEDBACK_SLUG


class SellingOnlineOverseasSuccessView(BaseSuccessView):
    slug = cms.GREAT_CONTACT_US_FORM_SUCCESS_SOO_SLUG


class GuidanceView(mixins.GetCMSPageMixin, TemplateView):
    template_name = 'contact/guidance.html'

    @property
    def slug(self):
        return self.kwargs['slug']


class SellingOnlineOverseasFormView(
    mixins.NotFoundOnDisabledFeature, mixins.PreventCaptchaRevalidationMixin,
    FormSessionMixin, mixins.PrepopulateFormMixin, NamedUrlSessionWizardView
):
    success_url = reverse_lazy('contact-us-selling-online-overseas-success')

    ORGANISATION = 'organisation'
    ORGANISATION_DETAILS = 'organisation-details'
    EXPERIENCE = 'your-experience'
    CONTACT_DETAILS = 'contact-details'

    form_list = (
        (ORGANISATION, forms.SellingOnlineOverseasBusiness),
        (ORGANISATION_DETAILS, forms.SellingOnlineOverseasBusinessDetails),
        (EXPERIENCE, forms.SellingOnlineOverseasExperience),
        (CONTACT_DETAILS, forms.SellingOnlineOverseasContactDetails),
    )

    templates = {
        ORGANISATION: 'contact/soo/step-organisation.html',
        ORGANISATION_DETAILS: 'contact/soo/step-organisation-details.html',
        EXPERIENCE: 'contact/soo/step-experience.html',
        CONTACT_DETAILS: 'contact/soo/step-contact-details.html',
    }

    def get(self, *args, **kwargs):
        market = self.request.GET.get('market')
        if market:
            self.request.session[SESSION_KEY_SOO_MARKET] = market
        return super().get(*args, **kwargs)

    @property
    def flag(self):
        return settings.FEATURE_FLAGS['SOO_CONTACT_FORM_ON']

    def get_template_names(self):
        return [self.templates[self.steps.current]]

    def get_form_kwargs(self, *args, **kwargs):
        # skipping `PrepopulateFormMixin.get_form_kwargs`
        return super(mixins.PrepopulateFormMixin, self).get_form_kwargs(
            *args, **kwargs
        )

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)
        if step == self.ORGANISATION and self.company_profile:
            initial.update({
                'soletrader': False,
                'company_name': self.company_profile['name'],
                'company_number': self.company_profile['number'],
                'company_postcode': self.company_profile['postal_code'],
                'website_address': self.company_profile['website'],
            })
        elif step == self.CONTACT_DETAILS and self.company_profile:
            initial.update({
                'contact_name': self.company_profile['postal_full_name'],
                'contact_email': self.request.sso_user.email,
                'phone': self.company_profile['mobile_number'],
            })
        return initial

    def serialize_form_list(self, form_list):
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)
        del data['terms_agreed']
        data['market'] = self.request.session.get(SESSION_KEY_SOO_MARKET)
        return data

    def get_context_data(self, **kwargs):
        return {
            'market_name': self.request.session.get(SESSION_KEY_SOO_MARKET),
            **super().get_context_data(**kwargs),
        }

    def done(self, form_list, **kwargs):
        form_data = self.serialize_form_list(form_list)
        sender = Sender(
            email_address=form_data['contact_email'],
            country_code=None
        )
        action = actions.ZendeskAction(
            subject=settings.CONTACT_SOO_ZENDESK_SUBJECT,
            full_name=form_data['contact_name'],
            email_address=form_data['contact_email'],
            service_name='soo',
            form_url=reverse(
                'contact-us-soo', kwargs={'step': 'organisation'}
            ),
            form_session=self.form_session,
            sender=sender,
        )
        response = action.save(form_data)
        response.raise_for_status()
        self.request.session.pop(SESSION_KEY_SOO_MARKET, None)
        return redirect(self.success_url)


class OfficeFinderFormView(
    mixins.NotFoundOnDisabledFeature, SubmitFormOnGetMixin, FormView
):
    template_name = 'contact/office-finder.html'
    form_class = forms.OfficeFinderForm

    @property
    def flag(self):
        return settings.FEATURE_FLAGS['OFFICE_FINDER_ON']

    @staticmethod
    def format_office_details(office_details):
        address = office_details['address_street'].split(', ')
        address.append(office_details['address_city'])
        address.append(office_details['address_postcode'])
        return {
            'address': '\n'.join(address),
            **office_details,
        }

    def form_valid(self, form):
        office_details = self.format_office_details(form.office_details)
        return TemplateResponse(
            self.request,
            self.template_name,
            {
                'office_details': office_details,
                **self.get_context_data(),
            }
        )


class OfficeContactFormView(
    mixins.NotFoundOnDisabledFeature, PrepopulateShortFormMixin,
    BaseNotifyFormView
):
    form_class = forms.TradeOfficeContactForm
    template_name = 'contact/domestic/step.html'

    @property
    def flag(self):
        return settings.FEATURE_FLAGS['OFFICE_FINDER_ON']

    @property
    def agent_email(self):
        return helpers.retrieve_exporting_advice_email(self.kwargs['postcode'])

    @property
    def notify_settings(self):
        return NotifySettings(
            agent_template=settings.CONTACT_OFFICE_AGENT_NOTIFY_TEMPLATE_ID,
            agent_email=self.agent_email,
            user_template=settings.CONTACT_OFFICE_USER_NOTIFY_TEMPLATE_ID,
        )

    def get_success_url(self):
        return reverse(
            'contact-us-office-success',
            kwargs={'postcode': self.kwargs['postcode']}
        )


class OfficeSuccessView(mixins.NotFoundOnDisabledFeature, BaseSuccessView):
    slug = cms.GREAT_CONTACT_US_FORM_SUCCESS_SLUG

    @property
    def flag(self):
        return settings.FEATURE_FLAGS['OFFICE_FINDER_ON']

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'next_url': reverse('landing-page'),
        }
