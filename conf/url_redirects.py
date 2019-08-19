from django.conf.urls import url
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView

from core.views import (
    OpportunitiesRedirectView, TranslationRedirectView, QuerystringRedirectView
)

redirects = [
    url(
        r'^story/online-marketplaces-propel-freestyle-xtreme-sales/$',
        QuerystringRedirectView.as_view(url=reverse_lazy('landing-page')),
        name='casestudy-online-marketplaces'
    ),
    url(
        r'^australia-event-calendar/$',
        QuerystringRedirectView.as_view(
            url='https://www.events.great.gov.uk/ehome/trade-events-calendar/all-events?keyword=australia'),
        name='australia-event-calendar'
    ),
    url(
        r'^(?i)trskorea/$',
        QuerystringRedirectView.as_view(
            url='https://eu.eventscloud.com/korea-uk-tech-rocketship-awards-kr'
        )
    ),
    url(
        r'^(?i)ukti/$',
        QuerystringRedirectView.as_view(url=reverse_lazy('landing-page'))
    ),
    url(
        r'^future/$',
        QuerystringRedirectView.as_view(
            url=(
                'https://www.events.great.gov.uk/ehome/index.php?'
                'eventid=200185206'
            ),
        )
    ),
    url(
        r'^(?i)innovation-hk/$',
        QuerystringRedirectView.as_view(
            url='https://www.events.great.gov.uk/ehome/innovation-hk',
        )
    ),
    url(
        r'^(?i)innovation-china/$',
        QuerystringRedirectView.as_view(
            url='https://www.events.great.gov.uk/ehome/innovation-china',
        )
    ),
    url(
        r'^(?i)innovation-asean/$',
        QuerystringRedirectView.as_view(
            url='https://www.events.great.gov.uk/ehome/innovation-asean',
        )
    ),
    url(
        r'^(?i)innovation-au-nz/$',
        QuerystringRedirectView.as_view(
            url='https://www.events.great.gov.uk/ehome/innovation-au-nz',
        )
    ),
    url(
        r'^(?i)innovation-jpn/$',
        QuerystringRedirectView.as_view(
            url='https://www.events.great.gov.uk/ehome/innovation-jpn',
        )
    ),
    url(
        r'^(?i)innovation-kor/$',
        QuerystringRedirectView.as_view(
            url='https://www.events.great.gov.uk/ehome/innovation-kor',
        )
    ),
    url(
        r'^bodw2019/$',
        QuerystringRedirectView.as_view(
            url='https://www.events.great.gov.uk/bodw2019/'),
    ),
    url(
        r'^events/$',
        QuerystringRedirectView.as_view(
            url='https://www.events.great.gov.uk/'),
    ),
    url(
        r'^expo2020/$',
        RedirectView.as_view(
            url='https://www.events.trade.gov.uk/dubai-expo-2020/'),
    ),
    url(
        r'^ukpavilion2020/$',
        RedirectView.as_view(
            url='https://www.events.trade.gov.uk/dubai-expo-2020/'
        ),
    ),
    url(
        r'^(?i)beijingexpo2019/$',
        RedirectView.as_view(
            url='https://www.events.great.gov.uk/ehome/index.php?eventid=200188985&'  # NOQA
        )
    ),
    url(
        r'^exporting-edge/$',
        RedirectView.as_view(pattern_name='get-finance'),
    ),
    url(
        r'^invest/$',
        QuerystringRedirectView.as_view(url='https://invest.great.gov.uk'),
    ),
    url(
        r'^int/invest/$',
        QuerystringRedirectView.as_view(url='https://invest.great.gov.uk/int'),
    ),
    url(
        r'^us/invest/$',
        QuerystringRedirectView.as_view(url='https://invest.great.gov.uk/us'),
    ),
    url(
        r'^es/invest/$',
        QuerystringRedirectView.as_view(url='https://invest.great.gov.uk/es'),
    ),
    url(
        r'^int/es/invest/$',
        QuerystringRedirectView.as_view(
            url='https://invest.great.gov.uk/int/es',
        ),
    ),
    url(
        r'^cn/invest/$',
        QuerystringRedirectView.as_view(url='https://invest.great.gov.uk/cn'),
    ),
    url(
        r'^int/zh/invest/$',
        QuerystringRedirectView.as_view(
            url='https://invest.great.gov.uk/int/zh',
        ),
    ),
    url(
        r'^int/pt/invest/$',
        QuerystringRedirectView.as_view(
            url='https://invest.great.gov.uk/int/pt',
        ),
    ),
    url(
        r'^br/invest/$',
        QuerystringRedirectView.as_view(url='https://invest.great.gov.uk/br'),
    ),
    url(
        r'^de/invest/$',
        QuerystringRedirectView.as_view(url='https://invest.great.gov.uk/de'),
    ),
    url(
        r'^int/de/invest/$',
        QuerystringRedirectView.as_view(
            url='https://invest.great.gov.uk/int/de',
        ),
    ),
    url(
        r'^jp/invest/$',
        QuerystringRedirectView.as_view(url='https://invest.great.gov.uk/jp'),
    ),
    url(
        r'^int/ja/invest/$',
        QuerystringRedirectView.as_view(
            url='https://invest.great.gov.uk/int/ja',
        ),
    ),
    url(
        r'^in/invest/$',
        QuerystringRedirectView.as_view(url='https://invest.great.gov.uk/in'),
    ),
    url(
        r'^int/ar/invest/$',
        QuerystringRedirectView.as_view(
            url='https://invest.great.gov.uk/int/ar',
        ),
    ),
    url(
        r'^study/$',
        QuerystringRedirectView.as_view(
            url='https://study-uk.britishcouncil.org',
        ),
    ),
    url(
        r'^visit/$',
        QuerystringRedirectView.as_view(
            url='https://www.visitbritain.com/gb/en',
        ),
    ),
    url(
        r'^export/$',
        QuerystringRedirectView.as_view(pattern_name='landing-page'),
    ),
    url(
        r'^export/new/$',
        QuerystringRedirectView.as_view(
            url='/advice/',
        ),
    ),
    url(
        r'^export/occasional/$',
        QuerystringRedirectView.as_view(
            url='/advice/',
        ),
    ),
    url(
        r'^export/regular/$',
        QuerystringRedirectView.as_view(
            url='/advice/',
        ),
    ),
    url(
        r'^export/opportunities/$',
        QuerystringRedirectView.as_view(
            url='https://opportunities.export.great.gov.uk/',
        ),
    ),
    url(
        r'^opportunities/$',
        QuerystringRedirectView.as_view(
            url='https://opportunities.export.great.gov.uk/',
        ),
    ),
    url(
        r'^opportunities/(?P<slug>[-\w]+)/$',
        # Redirects to https://opportunities.export.great.gov.uk/opportunities
        # with the slug and query parameters
        OpportunitiesRedirectView.as_view(),
    ),
    url(
        r'^export/find-a-buyer/$',
        QuerystringRedirectView.as_view(
            url='https://find-a-buyer.export.great.gov.uk',
        ),
    ),
    url(
        r'^export/selling-online-overseas/$',
        QuerystringRedirectView.as_view(
            url='https://selling-online-overseas.export.great.gov.uk',
        ),
    ),
    url(
        r'^uk/privacy-policy/$',
        QuerystringRedirectView.as_view(pattern_name='privacy-and-cookies'),
    ),
    url(
        r'^uk/terms-and-conditions/$',
        QuerystringRedirectView.as_view(pattern_name='terms-and-conditions'),
    ),
    url(
        r'^uk/$',
        TranslationRedirectView.as_view(pattern_name='landing-page'),
    ),
    url(
        r'^int/$',
        TranslationRedirectView.as_view(
            pattern_name='landing-page-international',
        ),
    ),
    url(
        r'^in/$',
        TranslationRedirectView.as_view(
            pattern_name='landing-page-international',
        ),
    ),
    url(
        r'^us/$',
        TranslationRedirectView.as_view(
            pattern_name='landing-page-international',
        ),
    ),
    url(
        r'^innovation/$',
        QuerystringRedirectView.as_view(
            url=(
                'https://www.events.trade.gov.uk/'
                'the-great-festival-of-innovation-hong-kong-2018/'
            ),
        ),
    ),
    url(
        r'^uk/cy/$',
        QuerystringRedirectView.as_view(
            url=(
                'https://www.great.gov.uk/?utm_source=Mailing&utm_medium'
                '=Brochure&utm_campaign=ExportBrochureCY'
            ),
        ),
    ),
    url(
        r'^verify/$',
        QuerystringRedirectView.as_view(
            url=(
                'https://find-a-buyer.export.great.gov.uk/'
                'verify/letter-confirm/'
            ),
        ),
    ),
    url(
        r'^legal/$',
        QuerystringRedirectView.as_view(
            url=(
                'https://trade.great.gov.uk/'
                'campaign/legal-is-great/singapore/'
            ),
        ),
    ),
    url(
        r'^kr/$',
        QuerystringRedirectView.as_view(
            url=(
                'https://www.events.trade.gov.uk/invest-in-great---korea'
                '?utm_source=print&utm_campaign=korean_winter_olympics_invest'
            )
        ),
    ),
]

# (<lang code path>, <language to use in query parameter>)
INTERNATIONAL_LANGUAGE_REDIRECTS_MAPPING = [
    ('de', 'de'),
    ('ar', 'ar'),
    ('zh', 'zh-hans'),
    ('pt', 'pt'),
    ('es', 'es'),
    ('ja', 'ja'),
]
international_redirects = [
    url(
        r'^int/{path}/$'.format(path=redirect[0]),
        TranslationRedirectView.as_view(
            pattern_name='landing-page-international',
            language=redirect[1],
        ),
    ) for redirect in INTERNATIONAL_LANGUAGE_REDIRECTS_MAPPING
]
# (<country code path>, <language to use in query parameter>)
INTERNATIONAL_COUNTRY_REDIRECTS_MAPPING = [
    ('cn', 'zh-hans'),
    ('br', 'pt'),
    ('jp', 'ja'),
]
international_redirects += [
    url(
        r'^{path}/$'.format(path=redirect[0]),
        TranslationRedirectView.as_view(
            pattern_name='landing-page-international',
            language=redirect[1],
        ),
    ) for redirect in (
            INTERNATIONAL_LANGUAGE_REDIRECTS_MAPPING +
            INTERNATIONAL_COUNTRY_REDIRECTS_MAPPING
    )
]

# TOS and privacy-and-cookies are no longer translated, instead we redirect to
# the ENG version
TOS_AND_PRIVACY_REDIRECT_LANGUAGES = (
    'zh', 'ja', r'es', 'pt', 'ar', 'de'
)

tos_redirects = [
    url(
        r'^int/{path}/terms-and-conditions/$'.format(path=language),
        QuerystringRedirectView.as_view(
            pattern_name='terms-and-conditions-international',
        ),
    ) for language in TOS_AND_PRIVACY_REDIRECT_LANGUAGES
]

privacy_redirects = [
    url(
        r'^int/{path}/privacy-policy/$'.format(
            path=language
        ),
        QuerystringRedirectView.as_view(
            pattern_name='privacy-and-cookies-international',
        ),
    ) for language in TOS_AND_PRIVACY_REDIRECT_LANGUAGES
]


contact_redirects = [
    url(
        r'^legacy/contact/(?P<service>[-\w\d]+)/FeedbackForm/$',
        QuerystringRedirectView.as_view(
            url=reverse_lazy('contact-us-feedback')
        ),
    ),
    url(
        r'^legacy/contact/feedback/(?P<service>[-\w\d]+)/$',
        QuerystringRedirectView.as_view(
            url=reverse_lazy('contact-us-feedback')
        ),
    ),
    url(
        r'^legacy/contact/feedback/$',
        QuerystringRedirectView.as_view(
            url=reverse_lazy('contact-us-feedback')
        ),
    ),
    url(
        r'^legacy/contact/(?P<service>[-\w\d]+)/feedback/$',
        QuerystringRedirectView.as_view(
            url=reverse_lazy('contact-us-feedback')
        ),
    ),
    url(
        r'^legacy/contact/single_sign_on/$',
        QuerystringRedirectView.as_view(
            url=reverse_lazy(
                'contact-us-routing-form', kwargs={'step': 'great-account'}
            )
        ),
    ),
    url(
        r'^legacy/contact/selling_online_overseas/$',
        QuerystringRedirectView.as_view(
            url=reverse_lazy(
                'contact-us-routing-form', kwargs={'step': 'domestic'}
            )
        ),
    ),
    url(
        r'^legacy/contact/export_ops/$',
        QuerystringRedirectView.as_view(
            url=reverse_lazy(
                'contact-us-routing-form', kwargs={'step': 'domestic'}
            )
        ),
    ),
    url(
        r'^legacy/contact/export_opportunities/$',
        QuerystringRedirectView.as_view(
            url=reverse_lazy(
                'contact-us-routing-form', kwargs={'step': 'domestic'}
            )
        ),
    ),
    url(
        r'^legacy/contact/cookies/$',
        QuerystringRedirectView.as_view(pattern_name='privacy-and-cookies'),
    ),
    url(
        r'^legacy/contact/terms-and-conditions/$',
        QuerystringRedirectView.as_view(pattern_name='terms-and-conditions'),
    ),
    # catch everything not covered above but not interfere with trailing slash
    # redirects
    url(
        r'^legacy/contact/(.*/)?$',
        QuerystringRedirectView.as_view(
            url=reverse_lazy(
                'contact-us-routing-form', kwargs={'step': 'location'}
            )
        ),
    ),
]

articles_redirects = [
    url(
        r'^market-research/$',
        QuerystringRedirectView.as_view(
            url='/advice/find-an-export-market/'
        )
    ),
    url(
        r'^market-research/do-research-first/$',
        QuerystringRedirectView.as_view(
            url='/advice/find-an-export-market/plan-export-market-research'
        )
    ),
    url(
        r'^market-research/define-market-potential/$',
        QuerystringRedirectView.as_view(
            url='/advice/find-an-export-market/define-export-market-potential'
        )
    ),
    url(
        r'^market-research/analyse-the-competition/$',
        QuerystringRedirectView.as_view(
            url='/advice/find-an-export-market/define-export-market-potential'
        )
    ),
    url(
        r'^market-research/research-your-market/$',
        QuerystringRedirectView.as_view(
            url='/advice/find-an-export-market/field-research-in-export-markets'  # NOQA
        )
    ),
    url(
        r'^market-research/visit-a-trade-show/$',
        QuerystringRedirectView.as_view(
            url='/advice/find-an-export-market/trade-shows'
        )
    ),
    url(
        r'^market-research/doing-business-with-integrity/$',
        QuerystringRedirectView.as_view(
            url='/advice/manage-legal-and-ethical-compliance/understand-business-risk-in-overseas-markets'  # NOQA
        )
    ),
    url(
        r'^market-research/know-the-relevant-legislation/$',
        QuerystringRedirectView.as_view(
            url='/advice/manage-legal-and-ethical-compliance/understand-business-risk-in-overseas-markets'  # NOQA
        )
    ),
    url(
        r'^business-planning/$',
        QuerystringRedirectView.as_view(
            url='/advice/define-route-to-market/'
        )
    ),
    url(
        r'^business-planning/make-an-export-plan/$',
        QuerystringRedirectView.as_view(
            url='/advice/create-an-export-plan/how-to-create-an-export-plan'
        )
    ),
    url(
        r'^business-planning/find-a-route-to-market/$',
        QuerystringRedirectView.as_view(
            url='/advice/define-route-to-market/routes-to-market'
        )
    ),
    url(
        r'^business-planning/sell-overseas-directly/$',
        QuerystringRedirectView.as_view(
            url='/advice/define-route-to-market/sell-overseas-directly'
        )
    ),
    url(
        r'^business-planning/use-an-overseas-agent/$',
        QuerystringRedirectView.as_view(
            url='/advice/define-route-to-market/export-agents'
        )
    ),
    url(
        r'^business-planning/choosing-an-agent-or-distributor/$',
        QuerystringRedirectView.as_view(
            url='/advice/define-route-to-market/export-agents'
        )
    ),
    url(
        r'^business-planning/use-a-distributor/$',
        QuerystringRedirectView.as_view(
            url='/advice/define-route-to-market/export-distributors'
        )
    ),
    url(
        r'^business-planning/license-your-product-or-service/$',
        QuerystringRedirectView.as_view(
            url='/advice/define-route-to-market/create-a-licensing-agreement'
        )
    ),
    url(
        r'^business-planning/licensing-and-franchising/$',
        QuerystringRedirectView.as_view(
            url='/advice/define-route-to-market/create-a-licensing-agreement'
        )
    ),
    url(
        r'^business-planning/franchise-your-business/$',
        QuerystringRedirectView.as_view(
            url='/advice/define-route-to-market/create-a-franchise-agreement'
        )
    ),
    url(
        r'^business-planning/start-a-joint-venture/$',
        QuerystringRedirectView.as_view(
            url='/advice/define-route-to-market/create-a-joint-venture-agreement'  # NOQA
        )
    ),
    url(
        r'^business-planning/set-up-an-overseas-operation/$',
        QuerystringRedirectView.as_view(
            url='/advice/define-route-to-market/set-up-a-business-abroad'
        )
    ),
    url(
        r'^finance/$',
        QuerystringRedirectView.as_view(
            url='/advice/get-export-finance-and-funding/'
        )
    ),
    url(
        r'^finance/choose-the-right-finance/$',
        QuerystringRedirectView.as_view(
            url='/advice/get-export-finance-and-funding/choose-the-right-finance'  # NOQA
        )
    ),
    url(
        r'^finance/get-money-to-export/$',
        QuerystringRedirectView.as_view(
            url='/advice/get-export-finance-and-funding/choose-the-right-finance'  # NOQA
        )
    ),
    url(
        r'^finance/get-export-finance/$',
        QuerystringRedirectView.as_view(
            url='/advice/get-export-finance-and-funding/get-export-finance'
        )
    ),
    url(
        r'^finance/get-finance-support-from-government/$',
        QuerystringRedirectView.as_view(
            url='/advice/get-export-finance-and-funding/get-export-finance'
        )
    ),
    url(
        r'^finance/raise-money-by-borrowing/$',
        QuerystringRedirectView.as_view(
            url='/advice/get-export-finance-and-funding/raise-money-by-borrowing'  # NOQA
        )
    ),
    url(
        r'^finance/borrow-against-assets/$',
        QuerystringRedirectView.as_view(
            url='/advice/get-export-finance-and-funding/borrow-against-assets'
        )
    ),
    url(
        r'^finance/raise-money-with-investment/$',
        QuerystringRedirectView.as_view(
            url='/advice/get-export-finance-and-funding/raise-money-with-investment'  # NOQA
        )
    ),
    url(
        r'^getting-paid/$',
        QuerystringRedirectView.as_view(
            url='/advice/manage-payment-for-export-orders/'
        )
    ),
    url(
        r'^getting-paid/invoice-currency-and-contents/$',
        QuerystringRedirectView.as_view(
            url='/advice/manage-payment-for-export-orders/payment-methods-for-exporters'  # NOQA
        )
    ),
    url(
        r'^getting-paid/consider-how-to-get-paid/$',
        QuerystringRedirectView.as_view(
            url='/advice/manage-payment-for-export-orders/how-to-create-an-export-invoice'  # NOQA
        )
    ),
    url(
        r'^getting-paid/decide-when-to-get-paid/$',
        QuerystringRedirectView.as_view(
            url='/advice/manage-payment-for-export-orders/decide-when-to-get-paid-for-export-orders'  # NOQA
        )
    ),
    url(
        r'^getting-paid/payment-methods/$',
        QuerystringRedirectView.as_view(
            url='/advice/manage-payment-for-export-orders/payment-methods-for-exporters'  # NOQA
        )
    ),
    url(
        r'^getting-paid/insure-against-non-payment/$',
        QuerystringRedirectView.as_view(
            url='/advice/manage-payment-for-export-orders/insure-against-non-payment'  # NOQA
        )
    ),
    url(
        r'^customer-insight/$',
        QuerystringRedirectView.as_view(
            url='/advice/prepare-to-do-business-in-a-foreign-country/'
        )
    ),
    url(
        r'^customer-insight/meet-your-customers/$',
        QuerystringRedirectView.as_view(
            url='/advice/prepare-to-do-business-in-a-foreign-country/understand-the-business-culture-in-the-market'  # NOQA
        )
    ),
    url(
        r'^customer-insight/know-your-customers/$',
        QuerystringRedirectView.as_view(
            url='/advice/manage-legal-and-ethical-compliance/understand-business-risk-in-overseas-markets'  # NOQA
        )
    ),
    url(
        r'^customer-insight/manage-language-differences/$',
        QuerystringRedirectView.as_view(
            url='/advice/prepare-to-do-business-in-a-foreign-country/understand-the-business-culture-in-the-market'  # NOQA
        )
    ),
    url(
        r'^customer-insight/understand-your-customers-culture/$',
        QuerystringRedirectView.as_view(
            url='/advice/prepare-to-do-business-in-a-foreign-country/understand-the-business-culture-in-the-market'  # NOQA
        )
    ),
    url(
        r'^operations-and-compliance/$',
        QuerystringRedirectView.as_view(
            url='/advice/manage-legal-and-ethical-compliance/'
        )
    ),
    url(
        r'^operations-and-compliance/internationalise-your-website/$',
        QuerystringRedirectView.as_view(
            url='/advice/prepare-to-do-business-in-a-foreign-country/internationalise-your-website'  # NOQA
        )
    ),
    url(
        r'^operations-and-compliance/match-your-website-to-your-audience/$',
        QuerystringRedirectView.as_view(
            url='/advice/prepare-to-do-business-in-a-foreign-country/internationalise-your-website'  # NOQA
        )
    ),
    url(
        r'^operations-and-compliance/protect-your-intellectual-property/$',
        QuerystringRedirectView.as_view(
            url='/advice/manage-legal-and-ethical-compliance/protect-your-intellectual-property-when-exporting'  # NOQA
        )
    ),
    url(
        r'^operations-and-compliance/types-of-intellectual-property/$',
        QuerystringRedirectView.as_view(
            url='/advice/manage-legal-and-ethical-compliance/protect-your-intellectual-property-when-exporting'  # NOQA
        )
    ),
    url(
        r'^operations-and-compliance/know-what-ip-you-have/$',
        QuerystringRedirectView.as_view(
            url='/advice/manage-legal-and-ethical-compliance/protect-your-intellectual-property-when-exporting'  # NOQA
        )
    ),
    url(
        r'^operations-and-compliance/international-ip-protection/$',
        QuerystringRedirectView.as_view(
            url='/advice/manage-legal-and-ethical-compliance/protect-your-intellectual-property-when-exporting'  # NOQA
        )
    ),
    url(
        r'^operations-and-compliance/report-corruption/$',
        QuerystringRedirectView.as_view(
            url='/advice/manage-legal-and-ethical-compliance/report-corruption-and-human-rights-violations'  # NOQA
        )
    ),
    url(
        r'^operations-and-compliance/anti-bribery-and-corruption-training/$',
        QuerystringRedirectView.as_view(
            url='/advice/manage-legal-and-ethical-compliance/anti-bribery-and-corruption-training'  # NOQA
        )
    ),
    url(
        r'^operations-and-compliance/plan-the-logistics/$',
        QuerystringRedirectView.as_view(
            url='/advice/prepare-for-export-procedures-and-logistics/plan-logistics-for-exporting'  # NOQA
        )
    ),
    url(
        r'^operations-and-compliance/get-your-export-documents-right/$',
        QuerystringRedirectView.as_view(
            url='/advice/prepare-for-export-procedures-and-logistics/get-your-export-documents-right'  # NOQA
        )
    ),
    url(
        r'^operations-and-compliance/use-a-freight-forwarder/$',
        QuerystringRedirectView.as_view(
            url='/advice/prepare-for-export-procedures-and-logistics/use-a-freight-forwarder-to-export'  # NOQA
        )
    ),
    url(
        r'^operations-and-compliance/use-incoterms-in-contracts/$',
        QuerystringRedirectView.as_view(
            url='/advice/prepare-for-export-procedures-and-logistics/use-incoterms-in-contracts'  # NOQA
        )
    ),
    url(
        r'^new/next-steps/$',
        QuerystringRedirectView.as_view(
            url='/advice/'
        )
    ),
    url(
        r'^occasional/next-steps/$',
        QuerystringRedirectView.as_view(
            url='/advice/'
        )
    ),
    url(
        r'^regular/next-steps/$',
        QuerystringRedirectView.as_view(
            url='/advice/'
        )
    ),
    url(
        r'^new/$',
        QuerystringRedirectView.as_view(
            url='/advice/'
        )
    ),
    url(
        r'^occasional/$',
        QuerystringRedirectView.as_view(
            url='/advice/'
        )
    ),
    url(
        r'^regular/$',
        QuerystringRedirectView.as_view(
            url='/advice/'
        )
    ),

    # CMS-1410 redirects for updated 'export advice' articles
    url(
        r'^advice/find-an-export-market/plan-export-market-research/$',
        QuerystringRedirectView.as_view(
            url='/advice/find-an-export-market/understand-export-market-research/'  # NOQA
        )
    ),
    url(
        r'^advice/find-an-export-market/define-export-market-potential/$',
        QuerystringRedirectView.as_view(
            url='/advice/find-an-export-market/research-export-markets-online/'
        )
    ),
    url(
        r'^advice/find-an-export-market/field-research-in-export-markets/$',
        QuerystringRedirectView.as_view(
            url='/advice/find-an-export-market/research-in-market/'
        )
    ),
    url(
        r'^advice/get-export-finance-and-funding/choose-the-right-finance/$',
        QuerystringRedirectView.as_view(
            url='/advice/get-export-finance-and-funding/understand-export-finance/'  # NOQA
        )
    ),
    url(
        r'^advice/get-export-finance-and-funding/raise-money-by-borrowing/$',
        QuerystringRedirectView.as_view(
            url='/advice/get-export-finance-and-funding/get-export-finance/'
        )
    ),
    url(
        r'^advice/get-export-finance-and-funding/borrow-against-assets/$',
        QuerystringRedirectView.as_view(
            url='/advice/get-export-finance-and-funding/get-export-finance/'
        )
    ),
    url(
        r'^advice/get-export-finance-and-funding/raise-money-with-investment/$',  # NOQA
        QuerystringRedirectView.as_view(
            url='/advice/get-export-finance-and-funding/get-export-finance/'
        )
    ),
]


redirects += (
        tos_redirects + contact_redirects + privacy_redirects +
        international_redirects + articles_redirects
)
