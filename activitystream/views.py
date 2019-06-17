import logging
from requests.exceptions import RequestException

from django.views.generic import TemplateView

from activitystream import helpers
from core.mixins import SetGA360ValuesMixin

logger = logging.getLogger(__name__)


class SearchView(SetGA360ValuesMixin, TemplateView):
    """ Search results page.

        URL parameters: 'q'    String to be searched
                        'page' Int results page number
    """
    template_name = 'search.html'
    page_type = 'SearchResultsPage'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        results = {}

        query = self.request.GET.get('q', '')
        page = helpers.sanitise_page(self.request.GET.get('page', '1'))
        elasticsearch_query = helpers.format_query(query, page)

        try:
            response = helpers.search_with_activitystream(elasticsearch_query)

        except RequestException:
            logger.error(
                "Activity Stream connection for "
                "Search failed. Query: '{}'".format(query))

            results = {
                'error_status_code': 500,
                'error_message': "Activity Stream connection failed",
                'query': query
            }

        else:
            if response.status_code != 200:
                results = {
                    'error_message': response.content,
                    'error_status_code': response.status_code,
                    'query': query
                }

            else:
                results = helpers.parse_results(response, query, page)

        return {**context, **results}


class SearchKeyPagesView(TemplateView):
    """ Returns data on key pages (such as the Get Finance homepage) to
        include in search that are otherwise not provided via other APIs.
    """
    template_name = 'search-key-pages.json'
