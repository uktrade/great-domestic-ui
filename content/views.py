from django.utils.functional import cached_property
from django.views.generic import TemplateView
from django.core.paginator import Paginator

from directory_constants import slugs

from directory_cms_client.client import cms_api_client

from .mixins import (
    GetCMSTagMixin,
    ArticleSocialLinksMixin,
)
from core.mixins import (
    PrototypeFeatureFlagMixin,
    NewsSectionFeatureFlagMixin,
    GetCMSPageMixin,
    GetCMSPageByPathMixin,
    SetGA360ValuesForCMSPageMixin,
    SetGA360ValuesMixin,
)

from core.helpers import handle_cms_response

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
    def filtered_countries(self):
        sector_id = self.request.GET.get('sector')

        if sector_id.isdigit() and int(sector_id) != 0:
            response = cms_api_client.lookup_countries_by_tag(tag_id=sector_id)
            return handle_cms_response(response)

        return None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        if self.filtered_countries:
            markets = self.filtered_countries['countries']
            tag_name = self.filtered_countries['name']
        else:
            markets = self.page['child_pages']
            tag_name = None

        sorted_markets = sorted(markets, key=lambda x: x['title'])

        paginator = Paginator(sorted_markets, 12)
        pagination_page = paginator.page(self.request.GET.get('page', 1))

        context['pagination_page'] = pagination_page
        context['filtered_countries'] = sorted_markets
        context['tag_name'] = tag_name
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


class NewsListPageView(
    NewsSectionFeatureFlagMixin, SetGA360ValuesMixin, GetCMSPageMixin, TemplateView,
):
    template_name = 'content/domestic_news_list.html'
    slug = slugs.EUEXIT_DOMESTIC_NEWS
    page_type = 'NewsList'


class NewsArticleDetailView(
    ArticleSocialLinksMixin,
    NewsSectionFeatureFlagMixin,
    GetCMSPageMixin,
    TemplateView,
):
    template_name = 'content/domestic_news_detail.html'

    @property
    def slug(self):
        return self.kwargs['slug']


class CommunityArticlePageView(CMSPageView):
    slug = 'community'
