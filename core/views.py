from directory_constants.constants import cms, urls
from directory_cms_client.client import cms_api_client
from directory_forms_api_client.helpers import FormSessionMixin, Sender

from django.conf import settings
from django.contrib import sitemaps
from django.http import JsonResponse
from django.urls import reverse, RegexURLResolver
from django.utils.cache import set_response_etag
from django.views.generic import FormView, TemplateView
from django.views.generic.base import RedirectView, View
from django.utils.functional import cached_property
from django.shortcuts import render

from casestudy import casestudies
from core import helpers, mixins, forms
from euexit.mixins import (
    HideLanguageSelectorMixin, EUExitFormsFeatureFlagMixin
)


class SetEtagMixin:
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if request.method == 'GET':
            response.add_post_render_callback(set_response_etag)
        return response


class LandingPageView(TemplateView):
    template_name = 'article/landing_page.html'

    @cached_property
    def page(self):
        response = cms_api_client.lookup_by_slug(
            slug=cms.GREAT_HOME_SLUG,
            draft_token=self.request.GET.get('draft_token'),
        )
        return helpers.handle_cms_response_allow_404(response)

    def get(self, request, *args, **kwargs):
        redirector = helpers.GeoLocationRedirector(self.request)
        if redirector.should_redirect:
            return redirector.get_response()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            page=self.page,
            casestudies=[
                casestudies.MARKETPLACE,
                casestudies.HELLO_BABY,
                casestudies.YORK,
            ],
            *args, **kwargs
        )


class CampaignPageView(
    mixins.CampaignPagesFeatureFlagMixin,
    mixins.GetCMSPageMixin,
    TemplateView
):
    template_name = 'core/campaign.html'

    @property
    def slug(self):
        return self.kwargs['slug']


class InternationalLandingPageView(
    mixins.TranslationsMixin,
    mixins.GetCMSPageMixin,
    mixins.GetCMSComponentMixin,
    TemplateView,
):
    template_name = 'core/landing_page_international.html'
    component_slug = cms.COMPONENTS_BANNER_INTERNATIONAL_SLUG
    slug = cms.GREAT_HOME_INTERNATIONAL_SLUG


class InternationalContactPageView(
    EUExitFormsFeatureFlagMixin,
    HideLanguageSelectorMixin,
    TemplateView,
):
    template_name = 'core/contact_page_international.html'

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            invest_contact_us_url=urls.build_invest_url('contact/'),
            *args, **kwargs
        )


class QuerystringRedirectView(RedirectView):
    query_string = True


class TranslationRedirectView(RedirectView):
    language = None
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        """
        Return the URL redirect
        """
        url = super().get_redirect_url(*args, **kwargs)

        if self.language:
            # Append 'lang' to query params
            if self.request.META.get('QUERY_STRING'):
                concatenation_character = '&'
            # Add 'lang' query param
            else:
                concatenation_character = '?'

            url = '{}{}lang={}'.format(
                url, concatenation_character, self.language
            )

        return url


class OpportunitiesRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        redirect_url = '{export_opportunities_url}{slug}/'.format(
            export_opportunities_url=(
                'https://opportunities.export.great.gov.uk/opportunities/'
            ),
            slug=kwargs.get('slug', '')
        )

        query_string = self.request.META.get('QUERY_STRING')
        if query_string:
            redirect_url = "{redirect_url}?{query_string}".format(
                redirect_url=redirect_url, query_string=query_string
            )

        return redirect_url


class InterstitialPageExoppsView(SetEtagMixin, TemplateView):
    template_name = 'core/interstitial_exopps.html'

    def get_context_data(self, **kwargs):
        context = {
            'exopps_url': settings.SERVICES_EXOPPS_ACTUAL
        }
        return context


class StaticViewSitemap(sitemaps.Sitemap):
    changefreq = 'daily'

    def items(self):
        # import here to avoid circular import
        from conf import urls
        from conf.url_redirects import redirects

        excluded_pages = [
            'triage-wizard'
        ]
        dynamic_cms_page_url_names = [
            'privacy-and-cookies-subpage',
            'contact-us-export-opportunities-guidance',
            'contact-us-great-account-guidance',
            'contact-us-export-advice',
            'contact-us-soo',
            'campaign-page',
            'contact-us-routing-form',
            'office-finder-contact',
            'contact-us-office-success',
            'report-ma-barrier'
        ]

        excluded_pages += dynamic_cms_page_url_names
        excluded_pages += [url.name for url in urls.article_urls]
        excluded_pages += [url.name for url in urls.news_urls]

        return [
            item.name for item in urls.urlpatterns
            if not isinstance(item, RegexURLResolver) and
            item not in redirects and
            item.name not in excluded_pages
        ]

    def location(self, item):
        if item == 'uk-export-finance-lead-generation-form':
            return reverse(item, kwargs={'step': 'contact'})
        elif item == 'report-ma-barrier':
            return reverse(item, kwargs={'step': 'about'})
        return reverse(item)


class AboutView(SetEtagMixin, TemplateView):
    template_name = 'core/about.html'


class PrivacyCookiesDomesticCMS(mixins.GetCMSPageMixin, TemplateView):
    template_name = 'core/info_page.html'
    slug = cms.GREAT_PRIVACY_AND_COOKIES_SLUG


class PrivacyCookiesDomesticSubpageCMS(mixins.GetCMSPageMixin, TemplateView):
    template_name = 'core/privacy_subpage.html'

    @property
    def slug(self):
        return self.kwargs['slug']


class PrivacyCookiesInternationalCMS(PrivacyCookiesDomesticCMS):
    template_name = 'core/info_page_international.html'


class TermsConditionsDomesticCMS(mixins.GetCMSPageMixin, TemplateView):
    template_name = 'core/info_page.html'
    slug = cms.GREAT_TERMS_AND_CONDITIONS_SLUG


class TermsConditionsInternationalCMS(TermsConditionsDomesticCMS):
    template_name = 'core/info_page_international.html'


class PerformanceDashboardView(
    mixins.PerformanceDashboardFeatureFlagMixin,
    mixins.GetCMSPageMixin,
    TemplateView
):
    template_name = 'core/performance_dashboard.html'


class PerformanceDashboardGreatView(PerformanceDashboardView):
    slug = cms.GREAT_PERFORMANCE_DASHBOARD_SLUG


class PerformanceDashboardExportOpportunitiesView(PerformanceDashboardView):
    slug = cms.GREAT_PERFORMANCE_DASHBOARD_EXOPPS_SLUG


class PerformanceDashboardSellingOnlineOverseasView(PerformanceDashboardView):
    slug = cms.GREAT_PERFORMANCE_DASHBOARD_SOO_SLUG


class PerformanceDashboardTradeProfilesView(PerformanceDashboardView):
    slug = cms.GREAT_PERFORMANCE_DASHBOARD_TRADE_PROFILE_SLUG


class PerformanceDashboardInvestView(PerformanceDashboardView):
    slug = cms.GREAT_PERFORMANCE_DASHBOARD_INVEST_SLUG


class PerformanceDashboardNotesView(PerformanceDashboardView):
    slug = cms.GREAT_PERFORMANCE_DASHBOARD_NOTES_SLUG
    template_name = 'core/performance_dashboard_notes.html'


class ServiceNoLongerAvailableView(TemplateView):
    template_name = 'core/service_no_longer_available.html'


class CompaniesHouseSearchApiView(View):
    form_class = forms.CompaniesHouseSearchForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(data=request.GET)
        if not form.is_valid():
            return JsonResponse(form.errors, status=400)
        api_response = helpers.CompaniesHouseClient.search(
            term=form.cleaned_data['term']
        )
        api_response.raise_for_status()
        return JsonResponse(api_response.json()['items'], safe=False)


class SendNotifyMessagesMixin:

    def send_agent_message(self, form):
        sender = Sender(
            email_address=form.cleaned_data['email'],
            country_code=None,
        )
        response = form.save(
            template_id=self.notify_settings.agent_template,
            email_address=self.notify_settings.agent_email,
            form_url=self.request.get_full_path(),
            form_session=self.form_session,
            sender=sender,
        )
        response.raise_for_status()

    def send_user_message(self, form):
        # no need to set `sender` as this is just a confirmation email.
        response = form.save(
            template_id=self.notify_settings.user_template,
            email_address=form.cleaned_data['email'],
            form_url=self.request.get_full_path(),
            form_session=self.form_session,
        )
        response.raise_for_status()

    def form_valid(self, form):
        self.send_agent_message(form)
        self.send_user_message(form)
        return super().form_valid(form)


class BaseNotifyFormView(FormSessionMixin, SendNotifyMessagesMixin, FormView):
    pass


class SearchView(TemplateView):
    ''' Search results. Note that this data is temporary and will be replaced with an API in time.
    '''
    def get(self, request, *args, **kwargs):
        results = [{
  "type": "Opportunities",
  "name": "Poland - Waste services",
  "content": "1) The subject of the contract covers the service of transport, management and/or neutralisation of hazardous and non-hazardous waste of the codes given in Appendix No. 1 to the ToR, from the area of real estate located in Głogów, at 8 Południowa Street, in the estimated quantity of approx. 3 600"
},
{
  "type": "Opportunities",
  "name": "France - Higher education services",
  "content": "Provision of teaching services in mathematics, physics, computer science and electronics (fundamental and applied) for candidates preparing for the internal competitions of the Directorate General of Civil Aviation (DGAC) and provision of services for export candidates."
},
{
  "type": "Opportunities",
  "name": "France - Data analysis services",
  "content": "The purpose of this contract is to analyze, retrieve and format data from the BPI sites in Jahia and create an export of this data for integration in Wordpress."
},
{
  "type": "Opportunities",
  "name": "Germany - snow clearing",
  "content": "Winter services for the properties1) Former procurement office of the Federal Customs Administration, Frankfurter Str. 91, 63067 Offenbach a. M.a) Public areas: 42.00 m2- Winter services: Mondays to Fridays for the first time until 06.00 a.m., end 20.00 a.m.; Saturdays, Sundays and public holidays in accordance with the statutesgb) Non-public areas: 1,327.00 m2- Winter services: Mondays to Fridays for the first time until 6.00 h, end 20.00 h2) Residential property, Strahlenberger Straße 149/149a, 63067 Offenbach a.M.- non-public areas: 28.00 m2, according to statutes3"
},
{
  "type": "Opportunities",
  "name": "Poland - Software package and information systems",
  "content": "The full scope of contract performance is included in the content of the Object of Contract, constituting Appendix No. 2 to the ToR1.. Implementation shall include, in particular, the following sub-stages:a) signing of the agreement together"
},
{
  "type": "Opportunities",
  "name": "Switzerland - IT services: Consulting, software development, internet and support",
  "content": "The service recipient procures a process- and workflow-supporting, parameterizable, intuitively operable, web-based overall solution for the migration system of the Canton of Berne, which is operated by the internal ICT service provider of the Canton of Berne.",
},
{
  "type": "Opportunities",
  "name": "France - Creation and maintenance of green spaces",
  "content": "Landscaping of the approach sections of urban agglomeration on departmental roads: - 2017 firm slice:-- Signalling, 530 half-days,-- Soil preparation, export/vegetable soil supply 1,850 m3, soil preparation 6,800 m2,-- Mulch installation 4,200 m2,-- Plant supply and planting 18,700 units,-- Grassing 6,200 m2,-- 18,700 shrubs, 6,200 m2 of grass,"
},
{
  "type": "Opportunities",
  "name": "Poland - Waste services",
  "content": "The subject of the contract is to equip all real estates inhabited in the Międzyrzecz commune with containers for collecting municipal waste and keeping them in a proper sanitary, clean and technical condition, as well as continuous and reliable collection of all municipal waste from all real estates in the period from"
},
{
  "type": "Advice",
  "name": "How to create an export plan",
  "content": "An export plan is a business plan for selling overseas. It should detail the decisions you’ve made based on your market research, your objectives and how you plan to achieve them."
},
{
  "type": "Opportunities",
  "name": "Poland - Air filters",
  "content": "The subject of this order is delivery, replacement, validation measurements, export and utilization of air filters in the buildings of the 600th anniversary of Jagiellonian University Renewal Campus in Krakow. In accordance with the table divided into buildings constituting Annex A and B to the ToR.",
  },
{
  "type": "Opportunities",
  "name": "France - Software maintenance and repair services",
  "content": "The \"Si_Di_Base_Export_Export_Prospect\" allows:- to store all data relating to prospective cases and contracts that have been concluded between French armaments manufacturers and foreign countries,- to be fully informed on the number, amounts and nature of contracts signed (statistical tool),"
}]
        return render(request, 'core/search.html', {'results': results })
