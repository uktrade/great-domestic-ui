from django.utils.functional import cached_property

from directory_cms_client.client import cms_api_client
from directory_components.helpers import SocialLinkBuilder

from core.helpers import handle_cms_response
from .helpers import unslugify


class GetCMSTagMixin:

    @cached_property
    def page(self):
        response = cms_api_client.lookup_by_tag(
            slug=self.slug,
            draft_token=self.request.GET.get('draft_token'),
        )
        return handle_cms_response(response)

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            tag_slug=self.slug,
            page=self.page,
            *args, **kwargs
        )


class ArticleSocialLinksMixin:

    @property
    def page_title(self):
        return self.page.get('article_title', '')

    def get_context_data(self, *args, **kwargs):

        social_links_builder = SocialLinkBuilder(
            self.request.build_absolute_uri(),
            self.page_title,
            'great.gov.uk')

        return super().get_context_data(
            social_links=social_links_builder.links,
            *args, **kwargs
        )
