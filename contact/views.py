from urllib.parse import urlparse

from directory_components.mixins import CountryDisplayMixin
from directory_constants import slugs, urls
from directory_forms_api_client import actions
from directory_forms_api_client.helpers import FormSessionMixin, Sender

from formtools.wizard.views import NamedUrlSessionWizardView

from django.conf import settings
from django.core.cache import cache
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.html import strip_tags
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.template.response import TemplateResponse
from django.utils.functional import cached_property

from core import mixins
from core.helpers import NotifySettings
from core.views import BaseNotifyFormView
from contact import constants, forms, helpers

SESSION_KEY_SOO_MARKET = 'SESSION_KEY_SOO_MARKET'
SOO_SUBMISSION_CACHE_TIMEOUT = 2592000  # 30 days


class ExportingToUKFormsFeatureFlagMixin(mixins.NotFoundOnDisabledFeature):
    @property
    def flag(self):
        return settings.FEATURE_FLAGS['EXPORTING_TO_UK_ON']


def build_export_opportunites_guidance_url(slug):
    return reverse_lazy(
        'contact-us-export-opportunities-guidance', kwargs={'slug': slug}
    )


def build_account_guidance_url(slug):
    return reverse_lazy(
        'contact-us-great-account-guidance', kwargs={'slug': slug}
    )


def build_exporting_guidance_url(slug):
    return reverse_lazy(
        'contact-us-exporting-to-the-uk-guidance', kwargs={'slug': slug}
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
        if self.request.user.is_authenticated and self.request.user.company:
            return {
                'email': self.request.user.email,
                'company_type': forms.LIMITED,
                'organisation_name': self.request.user.company['name'],
                'postcode': self.request.user.company['postal_code'],
                'given_name': self.guess_given_name,
                'family_name': self.guess_family_name,
            }


class PrepopulateInternationalFormMixin:

    def get_form_initial(self):
        if self.request.user.is_authenticated and self.request.user.company:
            return {
                'email': self.request.user.email,
                'organisation_name': self.request.user.company['name'],
                'country_name': self.request.user.company['country'],
                'city': self.request.user.company['locality'],
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
            sender=sender,
            subdomain=self.kwargs.get('zendesk_subdomain'),
        )
        response.raise_for_status()
        return super().form_valid(form)


class RoutingFormView(FormSessionMixin, NamedUrlSessionWizardView):

    # given the current step, based on selected  option, where to redirect.
    redirect_mapping = {
        constants.DOMESTIC: {
            constants.TRADE_OFFICE: reverse_lazy('office-finder'),
            constants.EXPORT_ADVICE: reverse_lazy(
                'contact-us-export-advice',
                kwargs={'step': 'comment'}
            ),
            constants.FINANCE: reverse_lazy(
                'uk-export-finance-lead-generation-form',
                kwargs={'step': 'contact'}
            ),
            constants.EUEXIT: reverse_lazy('brexit-contact-form'),
            constants.EVENTS: reverse_lazy('contact-us-events-form'),
            constants.DSO: reverse_lazy('contact-us-dso-form'),
            constants.OTHER: reverse_lazy('contact-us-enquiries'),
        },
        constants.INTERNATIONAL: {
            constants.INVESTING: settings.INVEST_CONTACT_URL,
            constants.CAPITAL_INVEST: settings.CAPITAL_INVEST_CONTACT_URL,
            constants.EXPORTING_TO_UK: build_exporting_guidance_url(
                slugs.HELP_EXPORTING_TO_UK
            ),
            constants.BUYING: settings.FIND_A_SUPPLIER_CONTACT_URL,
            constants.EUEXIT: settings.EU_EXIT_INTERNATIONAL_CONTACT_URL,
            constants.OTHER: reverse_lazy('contact-us-international'),
        },
        constants.EXPORT_OPPORTUNITIES: {
            constants.NO_RESPONSE: build_export_opportunites_guidance_url(
                slugs.HELP_EXOPPS_NO_RESPONSE
            ),
            constants.ALERTS: build_export_opportunites_guidance_url(
                slugs.HELP_EXOPP_ALERTS_IRRELEVANT
            ),
            constants.OTHER: reverse_lazy('contact-us-domestic'),
        },
        constants.GREAT_SERVICES: {
            constants.OTHER: reverse_lazy('contact-us-domestic'),
        },
        constants.GREAT_ACCOUNT: {
            constants.NO_VERIFICATION_EMAIL: build_account_guidance_url(
                slugs.HELP_MISSING_VERIFY_EMAIL
            ),
            constants.PASSWORD_RESET: build_account_guidance_url(
                slugs.HELP_PASSWORD_RESET
            ),
            constants.COMPANY_NOT_FOUND: build_account_guidance_url(
                slugs.HELP_ACCOUNT_COMPANY_NOT_FOUND
            ),
            constants.COMPANIES_HOUSE_LOGIN: build_account_guidance_url(
                slugs.HELP_COMPANIES_HOUSE_LOGIN
            ),
            constants.VERIFICATION_CODE: build_account_guidance_url(
                slugs.HELP_VERIFICATION_CODE_ENTER,
            ),
            constants.NO_VERIFICATION_LETTER: build_account_guidance_url(
                slugs.HELP_VERIFICATION_CODE_LETTER
            ),
            constants.NO_VERIFICATION_MISSING:
                build_account_guidance_url(
                slugs.HELP_VERIFICATION_CODE_MISSING
            ),
            constants.OTHER: reverse_lazy('contact-us-domestic'),
        },
        constants.EXPORTING_TO_UK: {
            constants.HMRC: settings.CONTACT_EXPORTING_TO_UK_HMRC_URL,
            constants.DEFRA: reverse_lazy(
                'contact-us-exporting-to-the-uk-defra'
            ),
            constants.BEIS: reverse_lazy(
                'contact-us-exporting-to-the-uk-beis'
            ),
            constants.IMPORT_CONTROLS: (
                reverse_lazy('contact-us-international')
            ),
            constants.TRADE_WITH_UK_APP: (
                reverse_lazy('contact-us-international')
            ),
            constants.OTHER: reverse_lazy('contact-us-international'),
        }
    }

    form_list = (
        (constants.LOCATION, forms.LocationRoutingForm),
        (constants.DOMESTIC, forms.DomesticRoutingForm),
        (constants.GREAT_SERVICES, forms.GreatServicesRoutingForm),
        (constants.GREAT_ACCOUNT, forms.GreatAccountRoutingForm),
        (constants.EXPORT_OPPORTUNITIES, forms.ExportOpportunitiesRoutingForm),
        (constants.INTERNATIONAL, forms.InternationalRoutingForm),
        (constants.EXPORTING_TO_UK, forms.ExportingIntoUKRoutingForm),
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
        constants.EXPORTING_TO_UK: 'contact/routing/step-exporting.html',
    }

    # given current step, where to send them back to
    back_mapping = {
        constants.DOMESTIC: constants.LOCATION,
        constants.INTERNATIONAL: constants.LOCATION,
        constants.GREAT_SERVICES: constants.DOMESTIC,
        constants.GREAT_ACCOUNT: constants.GREAT_SERVICES,
        constants.EXPORT_OPPORTUNITIES: constants.GREAT_SERVICES,
        constants.EXPORTING_TO_UK: constants.INTERNATIONAL,
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
        if self.request.user.is_authenticated and self.request.user.company:
            if step == self.PERSONAL:
                initial.update({
                    'email': self.request.user.email,
                    'phone': self.request.user.get_mobile_number(),
                    'first_name': self.guess_given_name,
                    'last_name': self.guess_family_name,
                })
            elif step == self.BUSINESS:
                sectors = self.request.user.company['sectors']
                initial.update({
                    'company_type': forms.LIMITED,
                    'companies_house_number': self.request.user.company['number'],
                    'organisation_name': self.request.user.company['name'],
                    'postcode': self.request.user.company['postal_code'],
                    'industry': sectors[0] if sectors else None,
                    'employees': self.request.user.company['employees'],
                })
        return initial

    def send_user_message(self, form_data):
        action = actions.GovNotifyEmailAction(
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
        if self.request.user.is_authenticated and self.request.user.company:
            return {
                'email': self.request.user.email,
                'name': self.request.user.get_full_name(),
            }


class DomesticFormView(PrepopulateShortFormMixin, BaseZendeskFormView):
    form_class = forms.ShortZendeskForm
    template_name = 'contact/domestic/step.html'
    success_url = reverse_lazy('contact-us-domestic-success')
    subject = settings.CONTACT_DOMESTIC_ZENDESK_SUBJECT


class DomesticEnquiriesFormView(PrepopulateShortFormMixin, BaseNotifyFormView):
    form_class = forms.ShortNotifyForm
    template_name = 'contact/domestic/step-enquiries.html'
    success_url = reverse_lazy('contact-us-domestic-success')
    notify_settings = NotifySettings(
        agent_template=settings.CONTACT_ENQUIRIES_AGENT_NOTIFY_TEMPLATE_ID,
        agent_email=settings.CONTACT_ENQUIRIES_AGENT_EMAIL_ADDRESS,
        user_template=settings.CONTACT_ENQUIRIES_USER_NOTIFY_TEMPLATE_ID,
    )


class InternationalFormView(
    mixins.PrepopulateFormMixin, PrepopulateInternationalFormMixin,
    BaseNotifyFormView
):
    form_class = forms.InternationalContactForm
    template_name = 'contact/international/step.html'
    success_url = reverse_lazy('contact-us-international-success')
    notify_settings = NotifySettings(
        agent_template=settings.CONTACT_INTERNATIONAL_AGENT_NOTIFY_TEMPLATE_ID,
        agent_email=settings.CONTACT_INTERNATIONAL_AGENT_EMAIL_ADDRESS,
        user_template=settings.CONTACT_INTERNATIONAL_USER_NOTIFY_TEMPLATE_ID,
    )


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


class GuidanceView(mixins.GetCMSPageMixin, TemplateView):
    template_name = 'contact/guidance.html'

    @property
    def slug(self):
        return self.kwargs['slug']


class ExortingToUKGuidanceView(
    ExportingToUKFormsFeatureFlagMixin,  mixins.GetCMSPageMixin, TemplateView
):
    template_name = 'contact/guidance-exporting-to-the-uk.html'

    @property
    def slug(self):
        return self.kwargs['slug']


# class WizardDynamicFormClassMixin(object):
#     def get_form_class(self, step):
#         return self.form_list[step]

#     def get_form(self, step=None, data=None, files=None):
#         """
#         Constructs the form for a given `step`. If no `step` is defined, the
#         current step will be determined automatically.

#         The form will be initialized using the `data` argument to prefill the
#         new form.
#         """
#         if step is None:
#             step = self.steps.current
#         # prepare the kwargs for the form instance.
#         kwargs = self.get_form_kwargs(step)
#         kwargs.update({
#             'data': data,
#             'files': files,
#             'prefix': self.get_form_prefix(step, self.form_list[step]),
#             'initial': self.get_form_initial(step),
#         })
#         return self.get_form_class(step)(**kwargs)


class SellingOnlineOverseasFormView(
    # WizardDynamicFormClassMixin,
    FormSessionMixin,
    mixins.PrepopulateFormMixin, NamedUrlSessionWizardView,
):
    success_url = reverse_lazy('contact-us-selling-online-overseas-success')
    CONTACT_DETAILS = 'contact-details'
    APPLICANT = 'applicant'
    APPLICANT_DETAILS = 'applicant-details'
    EXPERIENCE = 'your-experience'

    form_list = (
        (CONTACT_DETAILS, forms.SellingOnlineOverseasContactDetails),
        (APPLICANT, forms.SellingOnlineOverseasApplicantProxy),
        (APPLICANT_DETAILS, forms.SellingOnlineOverseasApplicantDetails),
        (EXPERIENCE, forms.SellingOnlineOverseasExperience),
    )

    templates = {
        CONTACT_DETAILS: 'contact/soo/step-contact-details.html',
        APPLICANT: 'contact/soo/step-applicant.html',
        APPLICANT_DETAILS: 'contact/soo/step-applicant-details.html',
        EXPERIENCE: 'contact/soo/step-experience.html',
    }

    def get(self, *args, **kwargs):
        market = self.request.GET.get('market')
        if market:
            self.request.session[SESSION_KEY_SOO_MARKET] = market
        return super().get(*args, **kwargs)

    def get_template_names(self):
        return [self.templates[self.steps.current]]

    # def get_form_kwargs(self, *args, **kwargs):
    #     # import pdb; pdb.set_trace()
        
    #         company_type = self.request.user.company['company_type']
    #     else:
    #         company_type = None
    #     return super(mixins.PrepopulateFormMixin, self).get_form_kwargs(*args, **kwargs)

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(mixins.PrepopulateFormMixin, self).get_form_kwargs(*args, **kwargs)
        # if self.request.user.company and 'company_type' in self.request.user.company:
        #     form_kwargs['company_type'] = self.request.user.company['company_type']
        # else:
        # import pdb; pdb.set_trace()
        # form_kwargs['company_type'] = 'ABC'
        return form_kwargs

    def get_cache_prefix(self):
        return 'selling_online_overseas_form_view_{}'.format(
            self.request.user.id)

    def get_form_data_cache(self):
        return cache.get(self.get_cache_prefix(), None)

    def set_form_data_cache(self, form_data):
        cache.set(self.get_cache_prefix(), form_data, SOO_SUBMISSION_CACHE_TIMEOUT)

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)
        if step == self.CONTACT_DETAILS:
            initial.update({
                'contact_first_name': self.request.user.first_name,
                'contact_last_name': self.request.user.last_name,
                'contact_email': self.request.user.email,
            })
            if self.request.user.company:
                initial.update({
                    'phone': self.request.user.company['mobile_number'],
                })
        elif step == self.APPLICANT:
            if self.request.user.company:
                address_1 = self.request.user.company['address_line_1']
                address_2 = self.request.user.company['address_line_2']
                address = ", ".join(filter(None, [address_1, address_2]))
                initial.update({
                    'company_name': self.request.user.company['name'],
                    'company_address': address,
                    'website_address': self.request.user.company['website'],
                })
                if 'number' in self.request.user.company:
                    initial.update({
                        'company_number': self.request.user.company['number']
                    })
        elif step == self.EXPERIENCE:
            if self.request.user.company:
                initial['description'] = self.request.user.company['summary']

        return initial

    def serialize_form_list(self, form_list):
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)
        data['market'] = self.request.session.get(SESSION_KEY_SOO_MARKET)
        return data

    def get_context_data(self, form, **kwargs):
        return {
            'market_name': self.request.session.get(SESSION_KEY_SOO_MARKET),
            **super().get_context_data(form, **kwargs),
        }

    # def get_form_class(self, step):
    #     if step == self.APPLICANT:
    #         # For the Limited Company flow, company_type is COMPANIES_HOUSE
    #         # Non-companies-house flow: CHARITY, PARTNERSHIP, SOLE_TRADER
    #         # and OTHER. For the Individual flow: None
    #         if self.request.user.company and 'company_type' in self.request.user.company:
    #             company_type = self.request.user.company['company_type']
    #         else:
    #             company_type = None

    #         if company_type is None:
    #             return forms.SellingOnlineOverseasApplicantIndividual
    #         elif company_type == 'COMPANIES_HOUSE':
    #             return forms.SellingOnlineOverseasApplicant
    #         return forms.SellingOnlineOverseasApplicantNonCH
    #     return super(SellingOnlineOverseasFormView, self).get_form_class(step)

    def done(self, form_list, **kwargs):
        form_data = self.serialize_form_list(form_list)
        sender = Sender(
            email_address=form_data['contact_email'],
            country_code=None
        )
        full_name = ('%s %s' % (
            form_data['contact_first_name'],
            form_data['contact_last_name']
        )).strip()
        action = actions.ZendeskAction(
            subject=settings.CONTACT_SOO_ZENDESK_SUBJECT,
            full_name=full_name,
            email_address=form_data['contact_email'],
            service_name='soo',
            form_url=reverse(
                'contact-us-soo', kwargs={'step': 'contact-details'}
            ),
            form_session=self.form_session,
            sender=sender,
        )
        response = action.save(form_data)
        response.raise_for_status()
        self.request.session.pop(SESSION_KEY_SOO_MARKET, None)
        self.set_form_data_cache(form_data)
        return redirect(self.success_url)


class OfficeFinderFormView(SubmitFormOnGetMixin, FormView):
    template_name = 'contact/office-finder.html'
    form_class = forms.OfficeFinderForm
    postcode = ''

    @cached_property
    def all_offices(self):
        return helpers.retrieve_regional_offices(
            self.postcode
        )

    def form_valid(self, form):
        self.postcode = form.cleaned_data['postcode']
        office_details = helpers.extract_regional_office_details(
            self.all_offices
        )
        other_offices = helpers.extract_other_offices_details(self.all_offices)
        return TemplateResponse(
            self.request,
            self.template_name,
            {
                'office_details': office_details,
                'other_offices': other_offices,
                **self.get_context_data(),
            }
        )


class OfficeContactFormView(PrepopulateShortFormMixin, BaseNotifyFormView):
    form_class = forms.TradeOfficeContactForm
    template_name = 'contact/domestic/step.html'

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


class ExportingToUKDERAFormView(
    ExportingToUKFormsFeatureFlagMixin,
    mixins.PrepopulateFormMixin,
    PrepopulateInternationalFormMixin,
    BaseNotifyFormView
):
    form_class = forms.InternationalContactForm
    template_name = 'contact/international/step.html'
    success_url = reverse_lazy('contact-us-exporting-to-the-uk-defra-success')
    notify_settings = NotifySettings(
        agent_template=settings.CONTACT_DEFRA_AGENT_NOTIFY_TEMPLATE_ID,
        agent_email=settings.CONTACT_DEFRA_AGENT_EMAIL_ADDRESS,
        user_template=settings.CONTACT_DEFRA_USER_NOTIFY_TEMPLATE_ID,
    )


class ExportingToUKBEISFormView(
    ExportingToUKFormsFeatureFlagMixin,
    mixins.PrepopulateFormMixin,
    PrepopulateInternationalFormMixin,
    BaseNotifyFormView
):
    form_class = forms.InternationalContactForm
    template_name = 'contact/international/step.html'
    success_url = reverse_lazy('contact-us-exporting-to-the-uk-beis-success')
    notify_settings = NotifySettings(
        agent_template=settings.CONTACT_BEIS_AGENT_NOTIFY_TEMPLATE_ID,
        agent_email=settings.CONTACT_BEIS_AGENT_EMAIL_ADDRESS,
        user_template=settings.CONTACT_BEIS_USER_NOTIFY_TEMPLATE_ID,
    )


class ExportingToUKFormView(
    ExportingToUKFormsFeatureFlagMixin,
    mixins.PrepopulateFormMixin,
    PrepopulateInternationalFormMixin,
    BaseZendeskFormView,
):
    form_class = forms.InternationalContactForm
    template_name = 'contact/international/step.html'
    success_url = reverse_lazy('contact-us-international-success')
    subject = settings.CONTACT_INTERNATIONAL_ZENDESK_SUBJECT


class BaseSuccessView(FormSessionMixin, mixins.GetCMSPageMixin, TemplateView):

    @property
    def slug(self):
        return self.kwargs['slug']

    def clear_form_session(self, response):
        self.form_session.clear()

    def get(self, *args, **kwargs):
        # setting ingress url not very meaningful here, so skip it.
        response = super(FormSessionMixin, self).get(*args, **kwargs)
        response.add_post_render_callback(self.clear_form_session)
        return response

    def get_next_url(self):
        # If the ingress URL is internal and it's not contact page then allow
        # user to go back to it
        parsed_url = urlparse(self.form_session.ingress_url)
        if (
            parsed_url.netloc == self.request.get_host() and
            not parsed_url.path.startswith('/contact')
        ):
            return self.form_session.ingress_url
        return reverse('landing-page')

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            **kwargs,
            next_url=self.get_next_url()
        )


class DomesticSuccessView(BaseSuccessView):
    template_name = 'contact/submit-success-domestic.html'


class InternationalSuccessView(CountryDisplayMixin, BaseSuccessView):
    template_name = 'contact/submit-success-international.html'


class OfficeSuccessView(DomesticSuccessView):
    slug = slugs.HELP_FORM_SUCCESS

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'next_url': reverse('landing-page'),
        }


class ExportingToUKSuccessView(
    ExportingToUKFormsFeatureFlagMixin, InternationalSuccessView
):
    pass


class SellingOnlineOverseasSuccessView(DomesticSuccessView):
    slug = slugs.HELP_FORM_SUCCESS_SOO

    def get_next_url(self):
        return urls.domestic.SELLING_OVERSEAS

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            **kwargs,
            next_url_text='Go back to Selling Online Overseas'
        )


class ExportVoucherFeatureFlagMixin(mixins.NotFoundOnDisabledFeature):
    @property
    def flag(self):
        return settings.FEATURE_FLAGS['EXPORT_VOUCHERS_ON']


class ExportVoucherFormView(ExportVoucherFeatureFlagMixin, mixins.SetGA360ValuesMixin, FormSessionMixin, FormView):
    page_type = 'ContactPage'
    template_name = 'contact/export-voucher-form.html'
    success_url = reverse_lazy('export-voucher-success')
    form_class = forms.ExportVoucherForm

    def form_valid(self, form):
        sender = Sender(
            email_address=form.cleaned_data['email'],
            country_code=None,
        )
        response = form.save(
            template_id=settings.EXPORT_VOUCHERS_GOV_NOTIFY_TEMPLATE_ID,
            email_address=settings.EXPORT_VOUCHERS_AGENT_EMAIL,
            form_url=self.request.get_full_path(),
            form_session=self.form_session,
            sender=sender,
        )
        response.raise_for_status()
        return super().form_valid(form)


class ExportVoucherSuccessView(ExportVoucherFeatureFlagMixin, mixins.SetGA360ValuesMixin, TemplateView):
    page_type = 'ContactPage'
    template_name = 'contact/export-voucher-success.html'
