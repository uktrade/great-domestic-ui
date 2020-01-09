from django.utils.functional import cached_property
from django.views.generic import TemplateView
from django.core.paginator import Paginator

from directory_cms_client.client import cms_api_client
from core import helpers

from .mixins import (
    GetCMSTagMixin,
    ArticleSocialLinksMixin,
)
from core.mixins import (
    PrototypeFeatureFlagMixin,
    GetCMSPageMixin,
    GetCMSPageByPathMixin,
    SetGA360ValuesForCMSPageMixin,
    SetGA360ValuesMixin,
)

from core.helpers import handle_cms_response_allow_404


TEMPLATE_MAPPING = {
    'TopicLandingPage': 'content/topic_list.html',
    'SuperregionPage': 'content/superregion.html',
    'CountryGuidePage': 'content/country_guide.html',
    'ArticleListingPage': 'content/article_list.html',
    'ArticlePage': 'content/article_detail.html',
    'MarketingArticlePage': 'content/marketing_article_detail.html',
    'CampaignPage': 'core/campaign.html',
    'PerformanceDashboardPage': 'core/performance_dashboard.html',
    'PerformanceDashboardNotesPage': 'core/performance_dashboard_notes.html',
    'PrivacyAndCookiesPage': 'core/info_page.html',
}


class TemplateChooserMixin:
    @property
    def template_name(self):
        return TEMPLATE_MAPPING[self.page['page_type']]


class CMSPageView(
    SetGA360ValuesForCMSPageMixin,
    ArticleSocialLinksMixin,
    TemplateChooserMixin,
    GetCMSPageMixin,
    TemplateView,
):
    @property
    def slug(self):
        return self.kwargs['slug']


class CMSPageFromPathView(SetGA360ValuesForCMSPageMixin, TemplateChooserMixin, GetCMSPageByPathMixin, TemplateView):
    pass


class MarketsPageView(CMSPageView):
    template_name = 'content/markets_landing_page.html'

    @cached_property
    def selected_sectors(self):
        return self.request.GET.getlist('sector')

    @cached_property
    def selected_regions(self):
        return self.request.GET.getlist('region')

    @cached_property
    def filtered_countries(self):
        response = cms_api_client.lookup_country_guides(
            industry=','.join(self.selected_sectors), region=','.join(self.selected_regions)
        )
        results = handle_cms_response_allow_404(response)
        # import pdb
        # pdb.set_trace()

        return self.sort_results(results)

    @cached_property
    def regions_list(self):
        return helpers.handle_cms_response(cms_api_client.list_regions())

    @cached_property
    def sector_list(self):
        return helpers.handle_cms_response(cms_api_client.list_industry_tags())

    def sortby_options(self):
        options = [
            {'value': 'title', 'label': 'Market A-Z'},
            {'value': 'region', 'label': 'Region'},
            {'value': 'last_published_at', 'label': 'Recently updated'},
        ]
        return options

    def sort_results(self, countries):
        print(countries)
        for country in countries:
            sortoption = self.request.GET.get('sortby')
            if sortoption and sortoption in countries[0] and country[sortoption] is None:
                return sorted(countries, key=lambda x: (x['title'] or '').replace('The ', ''))
            elif sortoption == 'region':
                return sorted(countries, key=lambda x: (x['region'] or '').replace('The ', ''))
            elif sortoption == 'last_published_at':
                return sorted(countries, key=lambda x: (x['last_published_at'] or ''), reverse=True)
            else:
                print('else', countries)
                return sorted(countries, key=lambda x: x['title'].replace('The ', ''))
        else:
            return countries

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        paginator = Paginator(self.filtered_countries, 18)
        pagination_page = paginator.page(self.request.GET.get('page', 1))
        context['sector_list'] = sorted(self.sector_list, key=lambda x: x['name'])
        context['regions_list'] = sorted(self.regions_list, key=lambda x: x['name'])
        context['selected_sectors'] = self.selected_sectors
        context['selected_regions'] = self.selected_regions
        context['sortby_options'] = self.sortby_options
        context['sortby'] = self.request.GET.get('sortby')
        context['pagination_page'] = pagination_page
        context['number_of_regions'] = len(self.selected_regions)
        context['number_of_results'] = len(self.filtered_countries)

        return context


class CountryGuidePageView(CMSPageView):
    num_of_statistics = 0
    section_three_num_of_subsections = 0

    def count_data_with_field(self, list_of_data, field):
        filtered_list = [item for item in list_of_data if item[field]]
        return len(filtered_list)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        self.num_of_statistics = self.count_data_with_field(
            context['page']['statistics'],
            'number'
        )
        fact_sheet = context['page']['fact_sheet']
        fact_sheet['num_of_columns'] = self.count_data_with_field(
            fact_sheet['columns'],
            'title'
        )
        for accordion in context['page']['accordions']:
            case_study = accordion['case_study']
            case_study['is_viable'] = \
                case_study['title'] and case_study['image']

            accordion['num_of_subsections'] = self.count_data_with_field(
                accordion['subsections'], 'heading')

            accordion['num_of_statistics'] = self.count_data_with_field(
                accordion['statistics'], 'number')

            accordion['neither_case_study_nor_statistics'] = \
                not case_study['is_viable'] and \
                not accordion['num_of_statistics']

            accordion['is_viable'] = \
                accordion['title'] and \
                accordion['teaser'] and \
                accordion['num_of_subsections'] >= 2

        context['market_guide_cta_text'] = (
            f"Exporting to {self.page['heading']} if there's no Brexit deal"
        )

        return context


class TagListPageView(
    PrototypeFeatureFlagMixin, SetGA360ValuesMixin, GetCMSTagMixin, TemplateView,
):
    template_name = 'content/tag_list.html'
    page_type = 'TagListPage'

    @property
    def slug(self):
        return self.kwargs['slug']


class CommunityArticlePageView(CMSPageView):
    slug = 'community'
