import logging
from requests.exceptions import RequestException

from django.views.generic import TemplateView
from django.conf import settings
from core import mixins
from activitystream import helpers

logger = logging.getLogger(__name__)


class SearchView(mixins.NotFoundOnDisabledFeature, TemplateView):
    """ Search results page.

        URL parameters: 'q'    String to be searched
                        'page' Int results page number
    """
    template_name = 'search.html'

    @property
    def flag(self):
        return settings.FEATURE_FLAGS['SEARCH_ON']

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('q', '')
        page = helpers.sanitise_page(self.request.GET.get('page', '1'))
        elasticsearch_query = helpers.format_query(query, page)

        try:
            response = helpers.search_with_activitystream(elasticsearch_query)
        except RequestException:
            logger.error(f"Activity Stream connection for\
 Search failed. Query: '{query}'")
            return {
                'error_status_code': 500,
                'error_message': "Activity Stream connection failed",
                'query': query
            }
        else:
            if response.status_code != 200:
                return {
                    'error_message': response.content,
                    'error_status_code': response.status_code,
                    'query': query
                }
            else:
                return helpers.parse_results(response, query, page)


class SearchKeyPagesView(TemplateView):
    """ Returns data on key pages (such as the Get Finance homepage) to
        include in search that are otherwise not provided via other APIs.
    """
    template_name = 'search-key-pages.json'
