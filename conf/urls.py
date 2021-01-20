from directory_constants import slugs

import directory_components.views
from directory_components.decorators import skip_ga360
from directory_constants.urls import international
import directory_healthcheck.views

from django.conf import settings
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.sitemaps.views import sitemap
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from core.views import QuerystringRedirectView

import content.views
import casestudy.views
import contact.views
import core.views
import euexit.views
import finance.views
import marketaccess.views
import community.views
import search.views
import ukef.views

from conf.url_redirects import redirects
from core.helpers import build_great_international_url


sitemaps = {
    'static': core.views.StaticViewSitemap,
}


urlpatterns = [
    url(
        r'^healthcheck/$',
        skip_ga360(directory_healthcheck.views.HealthcheckView.as_view()),
        name='healthcheck'
    ),
    url(
        r'^healthcheck/ping/$',
        skip_ga360(directory_healthcheck.views.PingView.as_view()),
        name='ping'
    ),
    url(
        r"^sitemap\.xml$",
        skip_ga360(sitemap),
        {'sitemaps': sitemaps},
        name='sitemap'
    ),
    url(
        r"^robots\.txt$",
        skip_ga360(directory_components.views.RobotsView.as_view()),
        name='robots'
    ),
    url(
        r"^not-found/$",
        skip_ga360(TemplateView.as_view(template_name='404.html')),
        name='not-found'
    ),
    url(
        r"^$",
        core.views.LandingPageView.as_view(),
        name='landing-page',
    ),
    url(
        r"^not-found/$",
        TemplateView.as_view(template_name='404.html'),
        name='not-found'
    ),
    url(
        r"^performance-dashboard/$",
        core.views.CMSPageView.as_view(),
        {'slug': slugs.PERFORMANCE_DASHBOARD},
        name='performance-dashboard'
    ),
    url(
        r"^performance-dashboard/export-opportunities/$",
        core.views.CMSPageView.as_view(),
        {'slug': slugs.PERFORMANCE_DASHBOARD_EXOPPS},
        name='performance-dashboard-export-opportunities'
    ),
    url(
        r"^performance-dashboard/selling-online-overseas/$",
        core.views.CMSPageView.as_view(),
        {'slug': slugs.PERFORMANCE_DASHBOARD_SOO},
        name='performance-dashboard-selling-online-overseas'
    ),
    url(
        r"^performance-dashboard/trade-profiles/$",
        core.views.CMSPageView.as_view(),
        {'slug': slugs.PERFORMANCE_DASHBOARD_TRADE_PROFILE},
        name='performance-dashboard-trade-profiles'
    ),
    url(
        r"^performance-dashboard/invest/$",
        core.views.CMSPageView.as_view(),
        {'slug': slugs.PERFORMANCE_DASHBOARD_INVEST},
        name='performance-dashboard-invest'
    ),
    url(
        r"^performance-dashboard/guidance-notes/$",
        core.views.CMSPageView.as_view(),
        {'slug': slugs.PERFORMANCE_DASHBOARD_NOTES},
        name='performance-dashboard-notes'
    ),
    # must come becore `campaigns/(?P<slug>[-\w\d]+)/$"`
    url(
        r"^campaigns/ecommerce-export-support/apply/$",
        contact.views.EcommerceSupportFormPageView.as_view(),
        name='ecommerce-export-support-form'
    ),
    url(
        r"^campaigns/ecommerce-export-support/success/$",
        skip_ga360(contact.views.ExportSupportSuccessPageView.as_view()),
        name='ecommerce-export-support-success'
    ),

    url(
        r"^campaigns/(?P<slug>[-\w\d]+)/$",
        core.views.OrphanCMSArticlePageView.as_view(),
        name='campaign-page'
    ),
    url(
        r"^services/$",
        core.views.ServicesView.as_view(),
        name='services'
    ),
    url(
        r"^privacy-and-cookies/$",
        core.views.PrivacyCookiesDomesticCMS.as_view(),
        name='privacy-and-cookies'
    ),
    url(
        r"^privacy-and-cookies/(?P<slug>[-\w\d]+)/$",
        core.views.CMSPageView.as_view(),
        name='privacy-and-cookies-subpage'
    ),
    url(
        r"^terms-and-conditions/$",
        core.views.TermsConditionsDomesticCMS.as_view(),
        name='terms-and-conditions'
    ),
    url(
        r"^accessibility-statement/$",
        core.views.AccessibilityStatementDomesticCMS.as_view(),
        name='accessibility-statement'
    ),
    url(
        r"^cookies/$",
        skip_ga360(
            core.views.CookiePreferencesPageView.as_view()),
        name='cookie-preferences'
    ),
    url(
        r"^export-opportunities/$",
        QuerystringRedirectView.as_view(url=settings.SERVICES_EXOPPS_ACTUAL),
        name='export-opportunities'
    ),
    url(
        r'^story/hello-babys-rapid-online-growth/$',
        casestudy.views.CasestudyHelloBabyView.as_view(),
        name='casestudy-hello-baby'
    ),
    url(
        r'^story/york-bag-retailer-goes-global-via-e-commerce/$',
        casestudy.views.CasestudyYorkBagView.as_view(),
        name='casestudy-york-bag'
    ),
    url(
        r'^get-finance/contact/thanks/$',
        skip_ga360(
            finance.views.GetFinanceLeadGenerationSuccessView.as_view()),
        name='uk-export-finance-lead-generation-form-success'
    ),
    url(
        r'^get-finance/(?P<step>.+)/$',
        skip_ga360(finance.views.GetFinanceLeadGenerationFormView.as_view(
            url_name='uk-export-finance-lead-generation-form',
            done_step_name='finished'
        )),
        name='uk-export-finance-lead-generation-form'
    ),
    url(
        r'^search/key-pages/$',
        skip_ga360(search.views.SearchKeyPagesView.as_view()),
        name='search-key-pages'
    ),
    url(
        r'^search/$',
        search.views.SearchView.as_view(),
        name='search'
    ),
    url(
        r'^search/feedback/$',
        search.views.SearchFeedbackFormView.as_view(),
        name='search-feedback'
    ),
    url(
        r'^search/test-api/$',
        skip_ga360(search.views.TestSearchAPIView.as_view()),
        name='search-test-api'
    )
]

legacy_urls = [
    url(
        r'^triage/(?P<step>.+)/$',
        skip_ga360(core.views.ServiceNoLongerAvailableView.as_view()),
        name='triage-wizard'
    ),
    url(
        r'^triage/$',
        skip_ga360(core.views.ServiceNoLongerAvailableView.as_view()),
        name='triage-start'
    ),
    url(
        r'^custom/$',
        skip_ga360(core.views.ServiceNoLongerAvailableView.as_view()),
        name='custom-page'
    ),
]


euexit_urls = [
    url(
        r'^transition-period/contact/$',
        euexit.views.DomesticContactFormView.as_view(),
        name='brexit-contact-form'
    ),
    url(
        r'^transition-period/contact/success/$',
        euexit.views.DomesticContactSuccessView.as_view(),
        name='brexit-contact-form-success'
    ),
]


article_urls = [
    url(
        r"^tagged/(?P<slug>[\w-]+)/$",
        content.views.TagListPageView.as_view(),
        name='tag-list',
    ),
    url(
        r"^advice/$",
        content.views.CMSPageView.as_view(),
        {'slug': 'advice'},
        name='advice',
    ),
    url(
        r"^advice/(?P<slug>[\w-]+)/$",
        content.views.CMSPageView.as_view(),
        name='advice-article-list',
    ),
    url(
        r"^advice/(?P<list>[\w-]+)/(?P<slug>[\w-]+)/$",
        content.views.CMSPageView.as_view(),
        name='advice-article',
    ),
    url(
        r"^markets/$",
        content.views.MarketsPageView.as_view(),
        {'slug': 'markets'},
        name='markets',
    ),
    url(
        r"^markets/(?P<slug>[\w-]+)/$",
        content.views.CountryGuidePageView.as_view(),
        name='country-guide',
    ),
]

contact_urls = [
    url(
        r'^contact/triage/export-opportunities/(?P<slug>[-\w\d]+)/$',
        skip_ga360(contact.views.GuidanceView.as_view()),
        name='contact-us-export-opportunities-guidance'
    ),
    url(
        r'^contact/triage/great-account/(?P<slug>[-\w\d]+)/$',
        skip_ga360(contact.views.GuidanceView.as_view()),
        name='contact-us-great-account-guidance'
    ),
    url(
        r'^contact/triage/international/(?P<slug>[-\w\d]+)/$',
        skip_ga360(contact.views.ExortingToUKGuidanceView.as_view()),
        name='contact-us-exporting-to-the-uk-guidance'
    ),
    url(
        r'^contact/events/$',
        skip_ga360(contact.views.EventsFormView.as_view()),
        name='contact-us-events-form'
    ),
    url(
        r'^contact/events/success/$',
        skip_ga360(contact.views.DomesticSuccessView.as_view()),
        {'slug': slugs.HELP_FORM_SUCCESS_EVENTS},
        name='contact-us-events-success'
    ),
    url(
        r'^contact/defence-and-security-organisation/$',
        skip_ga360(
            contact.views.DefenceAndSecurityOrganisationFormView.as_view()),
        name='contact-us-dso-form'
    ),
    url(
        r'^contact/defence-and-security-organisation/success/$',
        skip_ga360(contact.views.DomesticSuccessView.as_view()),
        {'slug': slugs.HELP_FORM_SUCCESS_DSO},
        name='contact-us-dso-success'
    ),
    url(
        r'^contact/export-advice/success/$',
        skip_ga360(contact.views.DomesticSuccessView.as_view()),
        {'slug': slugs.HELP_FORM_SUCCESS_EXPORT_ADVICE},
        name='contact-us-export-advice-success'
    ),
    url(
        r'^contact/export-advice/$',
        QuerystringRedirectView.as_view(url=reverse_lazy('contact-us-export-advice', kwargs={'step': 'comment'})),
        name='export-advice-routing-form'
    ),
    url(
        r'^contact/export-advice/(?P<step>.+)/$',
        skip_ga360(contact.views.ExportingAdviceFormView.as_view(
            url_name='contact-us-export-advice', done_step_name='finished'
        )),
        name='contact-us-export-advice'
    ),
    url(
        r'^contact/feedback/$',
        skip_ga360(contact.views.FeedbackFormView.as_view()),
        name='contact-us-feedback'
    ),
    url(
        r'^contact/feedback/success/$',
        skip_ga360(contact.views.DomesticSuccessView.as_view()),
        {'slug': slugs.HELP_FORM_SUCCESS_FEEDBACK},
        name='contact-us-feedback-success'
    ),
    url(
        r'^contact/domestic/$',
        skip_ga360(contact.views.DomesticFormView.as_view()),
        name='contact-us-domestic'
    ),
    url(
        r'^contact/domestic/enquiries/$',
        skip_ga360(contact.views.DomesticEnquiriesFormView.as_view()),
        name='contact-us-enquiries'
    ),
    url(
        r'^contact/domestic/success/$',
        skip_ga360(contact.views.DomesticSuccessView.as_view()),
        {'slug': slugs.HELP_FORM_SUCCESS},
        name='contact-us-domestic-success'
    ),
    url(
        r'^contact/international/$',
        skip_ga360(contact.views.InternationalFormView.as_view()),
        name='contact-us-international'
    ),
    url(
        r'^contact/international/success/$',
        skip_ga360(contact.views.InternationalSuccessView.as_view()),
        {'slug': slugs.HELP_FORM_SUCCESS_INTERNATIONAL},
        name='contact-us-international-success'
    ),
    url(
        r'^contact/selling-online-overseas/$',
        QuerystringRedirectView.as_view(
            url=reverse_lazy(
                'contact-us-soo', kwargs={'step': 'contact-details'}
            )
        ),
        name='contact-us-soo-redirect'
    ),
    url(
        r'^contact/selling-online-overseas/organisation/$',
        QuerystringRedirectView.as_view(
            url=reverse_lazy(
                'contact-us-soo', kwargs={'step': 'contact-details'}
            )
        ),
        name='contact-us-soo-organisation-redirect'
    ),
    url(
        r'^contact/selling-online-overseas/success/$',
        skip_ga360(contact.views.SellingOnlineOverseasSuccessView.as_view()),
        {'slug': slugs.HELP_FORM_SUCCESS_SOO},
        name='contact-us-selling-online-overseas-success'
    ),
    url(
        r'^contact/selling-online-overseas/(?P<step>.+)/$',
        login_required(skip_ga360(contact.views.SellingOnlineOverseasFormView.as_view(
            url_name='contact-us-soo', done_step_name='finished'
        ))),
        name='contact-us-soo'
    ),
    url(
        r'^contact/department-for-business-energy-and-industrial-strategy/$',
        skip_ga360(contact.views.ExportingToUKBEISFormView.as_view()),
        name='contact-us-exporting-to-the-uk-beis'
    ),
    url(
        (
            r'^contact/department-for-business-energy-and-industrial-strategy/'
            r'success/$'
        ),
        skip_ga360(contact.views.ExportingToUKSuccessView.as_view()),
        {'slug': slugs.HELP_FORM_SUCCESS_BEIS},
        name='contact-us-exporting-to-the-uk-beis-success'
    ),
    url(
        r'^contact/department-for-environment-food-and-rural-affairs/$',
        skip_ga360(contact.views.ExportingToUKDERAFormView.as_view()),
        name='contact-us-exporting-to-the-uk-defra'
    ),
    url(
        (
            r'^contact/department-for-environment-food-and-rural-affairs/'
            r'success/$'
        ),
        skip_ga360(contact.views.ExportingToUKSuccessView.as_view()),
        {'slug': slugs.HELP_FORM_SUCCESS_DEFRA},
        name='contact-us-exporting-to-the-uk-defra-success'
    ),
    url(
        r'^contact/exporting-to-the-uk/$',
        skip_ga360(contact.views.ExportingToUKFormView.as_view()),
        name='contact-us-exporting-to-the-uk'
    ),
    url(
        r'^contact/exporting-to-the-uk/import-controls/$',
        skip_ga360(contact.views.ExportingToUKFormView.as_view()),
        {'zendesk_subdomain': settings.EU_EXIT_ZENDESK_SUBDOMAIN},
        name='contact-us-exporting-to-the-uk-import-controls'
    ),
    url(
        r'^contact/exporting-to-the-uk/other/$',
        skip_ga360(contact.views.ExportingToUKFormView.as_view()),
        {'zendesk_subdomain': settings.EU_EXIT_ZENDESK_SUBDOMAIN},
        name='contact-us-exporting-to-the-uk-other'
    ),
    url(
        r'^contact/exporting-to-the-uk/trade-with-uk-app/$',
        skip_ga360(contact.views.ExportingToUKFormView.as_view()),
        name='contact-us-exporting-to-the-trade-with-uk-app'
    ),
    url(
        r'^contact/$',
        QuerystringRedirectView.as_view(
            url=reverse_lazy(
                'contact-us-routing-form', kwargs={'step': 'location'}
            )
        ),
        name='contact-us-routing-form-redirect'
    ),
    url(
        r'^contact/triage/(?P<step>.+)/$',
        skip_ga360(contact.views.RoutingFormView.as_view(
            url_name='contact-us-routing-form', done_step_name='finished'
        )),
        name='contact-us-routing-form'
    ),
    url(
        r'^contact/office-finder/$',
        skip_ga360(contact.views.OfficeFinderFormView.as_view()),
        name='office-finder'
    ),
    url(
        r'^contact/office-finder/(?P<postcode>[\w\d]+)/$',
        skip_ga360(contact.views.OfficeContactFormView.as_view()),
        name='office-finder-contact'
    ),
    url(
        r'^contact/office-finder/(?P<postcode>[\w\d]+)/success/$',
        skip_ga360(contact.views.OfficeSuccessView.as_view()),
        name='contact-us-office-success'
    ),
    url(
        r'^api/internal/companies-house-search/$',
        skip_ga360(core.views.CompaniesHouseSearchApiView.as_view()),
        name='api-internal-companies-house-search'
    ),
]

marketaccess_urls = [
    url(
        r'^report-trade-barrier/$',
        skip_ga360(marketaccess.views.MarketAccessView.as_view()),
        name='market-access'
    ),
    url(
        r'^report-trade-barrier/report/success/$',
        skip_ga360(
            marketaccess.views.ReportMarketAccessBarrierSuccessView.as_view()),
        name='report-barrier-form-success'
    ),
    url(
        r'^report-trade-barrier/report/(?P<step>.+)/$',
        skip_ga360(
            marketaccess.views.ReportMarketAccessBarrierFormView.as_view(
                url_name='report-ma-barrier',
                done_step_name='finished',
            )
        ),
        name='report-ma-barrier'
    ),

]

community_urls = [
    url(
        r"^community/join/$",
        community.views.CommunityJoinFormPageView.as_view(),
        name='community-join-form'
    ),
    url(
        r"^community/success/$",
        skip_ga360(community.views.CommunitySuccessPageView.as_view()),
        name='community-join-success'
    ),
    url(
        r'^community/$',
        content.views.CommunityArticlePageView.as_view(),
        name='community-article'
    ),
]

marketing_urls = [
    url(
        r"^local-export-support/apply/$",
        contact.views.ExportSupportFormPageView.as_view(),
        name='marketing-join-form'
        ),
    url(
        r"^local-export-support/success/$",
        skip_ga360(contact.views.ExportSupportSuccessPageView.as_view()),
        name='marketing-join-success'
    ),
]


ukef_urls = [
    url(
        r"^get-finance/$(?i)",
        skip_ga360(ukef.views.HomeView.as_view()),
        name='get-finance',
    ),
    url(
        r"^trade-finance/$(?i)",
        skip_ga360(finance.views.TradeFinanceView.as_view()),
        name='trade-finance'
    ),
    url(
        r"^project-finance/$(?i)",
        skip_ga360(ukef.views.LandingView.as_view()),
        name='project-finance',
    ),
    url(
        r"^uk-export-contact-form/$(?i)",
        skip_ga360(ukef.views.ContactView.as_view()),
        {'slug': 'uk-export-contact'},
        name='uk-export-contact',
    ),
    url(
        r"^uk-export-contact-form-success/$(?i)",
        skip_ga360(ukef.views.SuccessPageView.as_view()),
        name='uk-export-contract-success'
    ),
    url(
        r"^how-we-assess-your-project/$(?i)",
        skip_ga360(ukef.views.HowWeAssessPageView.as_view()),
        name='how-we-assess-your-project'
    ),
    url(
        r"^what-we-offer-you/$(?i)",
        skip_ga360(ukef.views.WhatWeOfferView.as_view()),
        name='what-we-offer-you'
    ),
    url(
        r"^country-cover/$(?i)",
        skip_ga360(ukef.views.CountryCoverView.as_view()),
        name='country-cover'
    ),
]

international_redirects_urls = [
    url(
        r'^trade/$',
        QuerystringRedirectView.as_view(url=international.TRADE_HOME),
        name='international-trade-home'
    ),
    url(
        r'^trade/(?P<path>[\w\-/]*)/$',
        QuerystringRedirectView.as_view(
            url=build_great_international_url('trade/incoming/%(path)s')),
        name='international-trade'
    ),
    url(
        r'^investment-support-directory/$',
        QuerystringRedirectView.as_view(url=international.EXPAND_ISD_HOME),
        name='international-investment-support-directory-home'
    ),
    url(
        r'^investment-support-directory/(?P<path>[\w\-/]*)/$',
        QuerystringRedirectView.as_view(url=build_great_international_url('investment-support-directory/%(path)s')),
        name='international-investment-support-directory'
    ),
]

export_vouchers_urls = [
    url(
        r'^export-vouchers/$',
        contact.views.ExportVoucherFormView.as_view(),
        name='export-voucher-form'
    ),
    url(
        r'^export-vouchers/sent/$',
        contact.views.ExportVoucherSuccessView.as_view(),
        name='export-voucher-success'
    )
]


urlpatterns += legacy_urls
urlpatterns += euexit_urls
urlpatterns += redirects
urlpatterns += article_urls
urlpatterns += contact_urls
urlpatterns += marketaccess_urls
urlpatterns += community_urls
urlpatterns += ukef_urls
urlpatterns += marketing_urls
urlpatterns += international_redirects_urls
urlpatterns += export_vouchers_urls

# Intentionally last in this file. Hardcoded urls above must always take priority
tree_based_cms_urls = [
    url(
        r'^(?P<path>[\w\-/]*)/$',
        content.views.CMSPageFromPathView.as_view(),
        name='tree-based-url'
    )
]

urlpatterns += tree_based_cms_urls
