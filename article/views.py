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
