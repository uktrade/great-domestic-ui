from directory_constants.constants import cms

from django.views.generic import TemplateView

from .mixins import (
    GetCMSTagMixin,
    ArticleSocialLinksMixin,
    BreadcrumbsMixin,
)
from core.mixins import (
    PrototypeFeatureFlagMixin,
    MarketsFeatureFlagMixin,
    NewsSectionFeatureFlagMixin,
    GetCMSComponentMixin,
    GetCMSPageMixin,
)
from euexit.mixins import HideLanguageSelectorMixin

TEMPLATE_MAPPING = {
    'TopicLandingPage': 'article/topic_list.html',
    'SuperregionPage': 'article/superregion.html',
    'CountryGuidePage': 'article/country_guide.html',
    'ArticleListingPage': 'article/article_list.html',
    'ArticlePage': 'article/article_detail.html'
}


class TemplateChooserMixin:
    @property
    def template_name(self):
        return TEMPLATE_MAPPING[self.page['page_type']]


class CMSPageView(
    BreadcrumbsMixin,
    ArticleSocialLinksMixin,
    TemplateChooserMixin,
    GetCMSPageMixin,
    TemplateView,
):
    @property
    def slug(self):
        return self.kwargs['slug']


class MarketsPageView(MarketsFeatureFlagMixin, CMSPageView):
    template_name = 'article/markets_landing_page.html'

    def get_context_data(self, **kwargs):
        context = super(MarketsPageView, self).get_context_data(**kwargs)

        def rename_heading_field(page):
            page['landing_page_title'] = page['heading']
            return page

        context['page']['child_pages'] = [rename_heading_field(child_page)
                                          for child_page
                                          in context['page']['child_pages']]
        return context


class CountryGuidePageView(MarketsFeatureFlagMixin, CMSPageView):
    num_of_statistics = 0
    section_three_num_of_subsections = 0

    def count_data_with_field(self, list_of_data, field):
        filtered_list = [item for item in list_of_data if item[field]]
        return len(filtered_list)

    def get_context_data(self, **kwargs):
        context = super(CountryGuidePageView, self).get_context_data(**kwargs)
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
                accordion['subsections'],
                'heading'
            )
            accordion['num_of_statistics'] = self.count_data_with_field(
                accordion['statistics'],
                'number'
            )
            accordion['num_of_ctas'] = self.count_data_with_field(
                accordion['ctas'],
                'link'
            )
            accordion['is_viable'] = \
                accordion['title'] and \
                accordion['teaser'] and \
                accordion['num_of_subsections'] >= 2 and \
                accordion['num_of_ctas'] >= 2
        return context


class TagListPageView(
    PrototypeFeatureFlagMixin,
    GetCMSTagMixin,
    TemplateView,
):
    template_name = 'article/tag_list.html'

    @property
    def slug(self):
        return self.kwargs['slug']


class NewsListPageView(
    NewsSectionFeatureFlagMixin,
    GetCMSPageMixin,
    TemplateView,
):
    template_name = 'article/domestic_news_list.html'
    slug = cms.GREAT_EU_EXIT_DOMESTIC_NEWS_SLUG


class NewsArticleDetailView(
    ArticleSocialLinksMixin,
    NewsSectionFeatureFlagMixin,
    GetCMSPageMixin,
    TemplateView,
):
    template_name = 'article/domestic_news_detail.html'

    @property
    def slug(self):
        return self.kwargs['slug']


class InternationalNewsListPageView(
    NewsSectionFeatureFlagMixin,
    GetCMSPageMixin,
    GetCMSComponentMixin,
    HideLanguageSelectorMixin,
    TemplateView,
):
    template_name = 'article/international_news_list.html'
    component_slug = cms.COMPONENTS_BANNER_DOMESTIC_SLUG
    slug = cms.GREAT_EU_EXIT_INTERNATIONAL_NEWS_SLUG


class InternationalNewsArticleDetailView(NewsArticleDetailView):
    template_name = 'article/international_news_detail.html'


class CommunityArticlePageView(CMSPageView):
    slug = 'community'
