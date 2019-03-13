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
    pass


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
        # self.section_three_num_of_subsections = self.count_data_with_field(
        #     context['page']['section_three_subsections'],
        #     'heading'
        # )
        for accordion in context['page']['accordions']:
            accordion['num_of_subsections'] = self.count_data_with_field(
                accordion['subsections'],
                'heading'
            )
            accordion['num_of_statistics'] = self.count_data_with_field(
                accordion['statistics'],
                'number'
            )
            # accordion['num_of_ctas'] = self.count_data_with_field(
            #     accordion['ctas'],
            #     'text'
            # )
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
