from directory_constants import slugs

import directory_components.views
from directory_components.decorators import skip_ga360
import directory_healthcheck.views

from django.conf import settings
from django.conf.urls import include, url
from django.contrib.sitemaps.views import sitemap
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

import article.views
import casestudy.views
import contact.views
import core.views
import euexit.views
import finance.views
import marketaccess.views
import community.views
import marketing.views
import search.views
import ukef.views

from conf.url_redirects import redirects


sitemaps = {
    'static': core.views.StaticViewSitemap,
}


healthcheck_urls = [
    url(
        r'^$',
        skip_ga360(directory_healthcheck.views.HealthcheckView.as_view()),
        name='healthcheck'
    ),
    url(
        r'^ping/$',
        skip_ga360(directory_healthcheck.views.PingView.as_view()),
        name='ping'
    ),
]


urlpatterns = [
    url(
        r'^healthcheck/',
        include(
            healthcheck_urls, namespace='healthcheck', app_name='healthcheck'
        )
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
    # The url below is feature flagged. Remove skip_ga360 and configure
    # ga360 data when it is enabled
    url(
        r"^campaigns/(?P<slug>[\w-]+)/$",
        skip_ga360(core.views.CampaignPageView.as_view()),
        name='campaign-page',
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
        r"^export-opportunities/$",
        RedirectView.as_view(
            url=settings.SERVICES_EXOPPS_ACTUAL,
            permanent=False
        ),
        name='export-opportunities'
    ),
    url(
        r'^story/hello-babys-rapid-online-growth/$',
        casestudy.views.CasestudyHelloBabyView.as_view(),
        name='casestudy-hello-baby'
    ),
    url(
        r'^story/online-marketplaces-propel-freestyle-xtreme-sales/$',
        casestudy.views.CasestudyMarketplaceView.as_view(),
        name='casestudy-online-marketplaces'
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

deprecated_urls = [
    # URLS TO BE REMOVED
    url(
        r"^about/$",
        skip_ga360(core.views.AboutView.as_view()),
        name='about'
    ),
    url(
        r"^international/$",
        skip_ga360(core.views.InternationalLandingPageView.as_view()),
        name='landing-page-international'
    ),
    url(
        r"^international/contact/$",
        skip_ga360(core.views.InternationalContactPageView.as_view()),
        name='contact-page-international'
    ),
    url(
        r"^international/privacy-and-cookies/$",
        skip_ga360(core.views.PrivacyCookiesInternationalCMS.as_view()),
        name='privacy-and-cookies-international'
    ),
    url(
        r"^international/terms-and-conditions/$",
        skip_ga360(core.views.TermsConditionsInternationalCMS.as_view()),
        name='terms-and-conditions-international'
    ),
    url(
        r'^international/eu-exit-news/contact/$',
        skip_ga360(euexit.views.InternationalContactFormView.as_view()),
        name='eu-exit-international-contact-form'
    ),
    url(
        r'^international/eu-exit-news/contact/success/$',
        skip_ga360(euexit.views.InternationalContactSuccessView.as_view()),
        name='eu-exit-international-contact-form-success'
    ),
    url(
        r"^international/eu-exit-news/$",
        skip_ga360(article.views.InternationalNewsListPageView.as_view()),
        name='international-eu-exit-news-list',
    ),
    url(
        r"^international/eu-exit-news/(?P<slug>[\w-]+)/$",
        skip_ga360(article.views.InternationalNewsArticleDetailView.as_view()),
        name='international-eu-exit-news-detail',
    ),
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
        r'^eu-exit-news/contact/$',
        euexit.views.DomesticContactFormView.as_view(),
        name='eu-exit-domestic-contact-form'
    ),
    url(
        r'^eu-exit-news/contact/success/$',
        euexit.views.DomesticContactSuccessView.as_view(),
        name='eu-exit-domestic-contact-form-success'
    ),
]


news_urls = [
    url(
        r"^eu-exit-news/$",
        article.views.NewsListPageView.as_view(),
        name='eu-exit-news-list',
    ),
    url(
        r"^eu-exit-news/(?P<slug>[\w-]+)/$",
        article.views.NewsArticleDetailView.as_view(),
        name='eu-exit-news-detail',
    ),
]


article_urls = [
    url(
        r"^tagged/(?P<slug>[\w-]+)/$",
        article.views.TagListPageView.as_view(),
        name='tag-list',
    ),
    url(
        r"^advice/$",
        article.views.CMSPageView.as_view(),
        {'slug': 'advice'},
        name='advice',
    ),
    url(
        r"^advice/create-an-export-plan/$",
        article.views.CMSPageView.as_view(),
        {'slug': 'create-an-export-plan'},
        name='create-an-export-plan',
    ),
    url(
        r"^advice/create-an-export-plan/(?P<slug>[\w-]+)/$",
        article.views.CMSPageView.as_view(),
        name='create-an-export-plan-article',
    ),
    url(
        r"^advice/find-an-export-market/$",
        article.views.CMSPageView.as_view(),
        {'slug': 'find-an-export-market'},
        name='find-an-export-market',
    ),
    url(
        r"^advice/find-an-export-market/(?P<slug>[\w-]+)/$",
        article.views.CMSPageView.as_view(),
        name='find-an-export-market-article',
    ),
    url(
        r"^advice/define-route-to-market/$",
        article.views.CMSPageView.as_view(),
        {'slug': 'define-route-to-market'},
        name='define-route-to-market',
    ),
    url(
        r"^advice/define-route-to-market/(?P<slug>[\w-]+)/$",
        article.views.CMSPageView.as_view(),
        name='define-route-to-market-article',
    ),
    url(
        r"^advice/get-export-finance-and-funding/$",
        article.views.CMSPageView.as_view(),
        {'slug': 'get-export-finance-and-funding'},
        name='get-export-finance-and-funding',
    ),
    url(
        r"^advice/get-export-finance-and-funding/(?P<slug>[\w-]+)/$",
        article.views.CMSPageView.as_view(),
        name='get-export-finance-and-funding-article',
    ),
    url(
        r"^advice/manage-payment-for-export-orders/$",
        article.views.CMSPageView.as_view(),
        {'slug': 'manage-payment-for-export-orders'},
        name='manage-payment-for-export-orders',
    ),
    url(
        r"^advice/manage-payment-for-export-orders/(?P<slug>[\w-]+)/$",
        article.views.CMSPageView.as_view(),
        name='manage-payment-for-export-orders-article',
    ),
    url(
        r"^advice/prepare-to-do-business-in-a-foreign-country/$",
        article.views.CMSPageView.as_view(),
        {'slug': 'prepare-to-do-business-in-a-foreign-country'},
        name='prepare-to-do-business-in-a-foreign-country',
    ),
    url(
        r"^advice/prepare-to-do-business-in-a-foreign-country/(?P<slug>[\w-]+)/$",  # noqa
        article.views.CMSPageView.as_view(),
        name='prepare-to-do-business-in-a-foreign-country-article',
    ),
    url(
        r"^advice/manage-legal-and-ethical-compliance/$",
        article.views.CMSPageView.as_view(),
        {'slug': 'manage-legal-and-ethical-compliance'},
        name='manage-legal-and-ethical-compliance',
    ),
    url(
        r"^advice/manage-legal-and-ethical-compliance/(?P<slug>[\w-]+)/$",
        article.views.CMSPageView.as_view(),
        name='manage-legal-and-ethical-compliance-article',
    ),
    url(
        r"^advice/prepare-for-export-procedures-and-logistics/$",
        article.views.CMSPageView.as_view(),
        {'slug': 'prepare-for-export-procedures-and-logistics'},
        name='prepare-for-export-procedures-and-logistics',
    ),
    url(
        r"^advice/prepare-for-export-procedures-and-logistics/(?P<slug>[\w-]+)/$",  # noqa
        article.views.CMSPageView.as_view(),
        name='prepare-for-export-procedures-and-logistics-article',
    ),
    url(
        r"^markets/$",
        article.views.MarketsPageView.as_view(),
        {'slug': 'markets'},
        name='markets',
    ),
    url(
        r"^markets/(?P<slug>[\w-]+)/$",
        article.views.CountryGuidePageView.as_view(),
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
        RedirectView.as_view(
            url=reverse_lazy(
                'contact-us-export-advice', kwargs={'step': 'comment'}
            )
        ),
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
        RedirectView.as_view(
            url=reverse_lazy(
                'contact-us-soo', kwargs={'step': 'organisation'}
            )
        ),
        name='contact-us-soo-redirect'
    ),
    url(
        r'^contact/selling-online-overseas/success/$',
        skip_ga360(contact.views.SellingOnlineOverseasSuccessView.as_view()),
        {'slug': slugs.HELP_FORM_SUCCESS_SOO},
        name='contact-us-selling-online-overseas-success'
    ),
    url(
        r'^contact/selling-online-overseas/(?P<step>.+)/$',
        skip_ga360(contact.views.SellingOnlineOverseasFormView.as_view(
            url_name='contact-us-soo', done_step_name='finished'
        )),
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
        RedirectView.as_view(
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
        article.views.CommunityArticlePageView.as_view(),
        name='community-article'
    ),
]

marketing_urls = [
    url(
            r"^marketing/join/$",
            marketing.views.MarketingJoinFormPageView.as_view(),
            name='marketing-join-form'
        ),
    url(
            r"^marketing/success/$",
            skip_ga360(community.views.CommunitySuccessPageView.as_view()),
            name='marketing-join-success'
        ),
]


ukef_urls = [
    url(
        r"^(?i)get-finance/$",
        skip_ga360(ukef.views.HomeView.as_view()),
        name='get-finance',
    ),
    url(
        r"^(?i)trade-finance/$",
        skip_ga360(finance.views.TradeFinanceView.as_view()),
        name='trade-finance'
    ),
    url(
        r"^(?i)project-finance/$",
        skip_ga360(ukef.views.LandingView.as_view()),
        name='project-finance',
    ),
    url(
        r"^(?i)uk-export-contact-form/$",
        skip_ga360(ukef.views.ContactView.as_view()),
        {'slug': 'uk-export-contact'},
        name='uk-export-contact',
    ),
    url(
        r"^(?i)uk-export-contact-form-success/$",
        skip_ga360(ukef.views.SuccessPageView.as_view()),
        name='uk-export-contract-success'
    ),
    url(
        r"^(?i)how-we-assess-your-project/$",
        skip_ga360(ukef.views.HowWeAssessPageView.as_view()),
        name='how-we-assess-your-project'
    ),
    url(
        r"^(?i)what-we-offer-you/$",
        skip_ga360(ukef.views.WhatWeOfferView.as_view()),
        name='what-we-offer-you'
    ),
    url(
        r"^(?i)country-cover/$",
        skip_ga360(ukef.views.CountryCoverView.as_view()),
        name='country-cover'
    ),
]

urlpatterns += legacy_urls
urlpatterns += deprecated_urls
urlpatterns += euexit_urls
urlpatterns += redirects
urlpatterns += news_urls
urlpatterns += article_urls
urlpatterns += contact_urls
urlpatterns += marketaccess_urls
urlpatterns += community_urls
urlpatterns += ukef_urls
urlpatterns += marketing_urls
