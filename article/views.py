from directory_constants import slugs

from django.views.generic import TemplateView

from directory_components.mixins import CountryDisplayMixin

from .mixins import (
    GetCMSTagMixin,
    ArticleSocialLinksMixin,
)
from core.mixins import (
    PrototypeFeatureFlagMixin,
    NewsSectionFeatureFlagMixin,
    GetCMSComponentMixin,
    GetCMSPageMixin,
    SetGA360ValuesForCMSPageMixin,
)

from euexit.mixins import HideLanguageSelectorMixin

TEMPLATE_MAPPING = {
    'TopicLandingPage': 'article/topic_list.html',
    'SuperregionPage': 'article/superregion.html',
    'CountryGuidePage': 'article/country_guide.html',
    'ArticleListingPage': 'article/article_list.html',
    'ArticlePage': 'article/article_detail.html',
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


class MarketsPageView(CMSPageView):
    template_name = 'article/markets_landing_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        def rename_heading_field(page):
            page['landing_page_title'] = page['heading']
            return page

        context['page']['child_pages'] = [
            rename_heading_field(child_page)
            for child_page in context['page']['child_pages']
        ]
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
            f"Exporting to {self.page['heading']} if there's no EU Exit deal"
        )

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
    slug = slugs.EUEXIT_DOMESTIC_NEWS


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
    CountryDisplayMixin,
    NewsSectionFeatureFlagMixin,
    GetCMSPageMixin,
    GetCMSComponentMixin,
    HideLanguageSelectorMixin,
    TemplateView,
):
    template_name = 'article/international_news_list.html'
    component_slug = slugs.COMPONENTS_BANNER_DOMESTIC
    slug = slugs.EUEXIT_INTERNATIONAL_NEWS


class InternationalNewsArticleDetailView(
    CountryDisplayMixin,
    NewsArticleDetailView
):
    template_name = 'article/international_news_detail.html'


class CommunityArticlePageView(CMSPageView):
    slug = 'community'
