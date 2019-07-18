from datetime import datetime
import logging
from requests.exceptions import RequestException

from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from core.mixins import SetGA360ValuesMixin
from search import helpers, forms
from search.mixins import TestSearchAPIFeatureFlagMixin

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
        import pdb; pdb.set_trace();

        results = {}
        query = self.request.GET.get('q', '')
        submitted = self.request.GET.get('submitted', '')
        page = helpers.sanitise_page(self.request.GET.get('page', '1'))

        common = {
            'submitted': submitted,
            'query': query,
            'current_page': page
        }

        try:
            elasticsearch_query = helpers.format_query(query, page)
            response = helpers.search_with_activitystream(elasticsearch_query)
            import pdb; pdb.set_trace();
        except RequestException:
            logger.error(
                "Activity Stream connection for "
                "Search failed. Query: '{}'".format(query))
            results = {
                'error_status_code': 500,
                'error_message': "Activity Stream connection failed"
            }
        else:
            if response.status_code != 200:
                results = {
                    'error_message': response.content,
                    'error_status_code': response.status_code
                }

            else:
                results = helpers.parse_results(
                    response, query, page
                )

        return {**context, **common, **results}


class SearchKeyPagesView(TemplateView):
    """ Returns data on key pages (such as the Get Finance homepage) to
        include in search that are otherwise not provided via other APIs.
    """
    template_name = 'search-key-pages.json'


class SearchFeedbackFormView(SetGA360ValuesMixin, FormView):
    template_name = 'search_feedback.html'
    form_class = forms.FeedbackForm
    page_type = 'SearchFeedbackPage'

    def get_success_url(self):
        page = self.request.POST['from_search_page']
        query = self.request.POST['from_search_query']
        return f"{reverse_lazy('search')}\
?page={page}&q={query}&submitted=true"

    #
    # email_address and full_name are required by FormsAPI.
    # However, in the UI, the user is given the option
    # to give contact details or not. Therefore defaults
    # are submitted if the user does not want to be contacted
    # to appease FormsAPI.
    #
    def form_valid(self, form):
        email = form.cleaned_data['contact_email'] or \
            "emailnotgiven@example.com"
        name = form.cleaned_data['contact_name'] or \
            "Name not given"
        subject = 'Search Feedback - ' + \
            datetime.now().strftime("%H:%M %d %b %Y")

        response = form.save(
            email_address=email,
            full_name=name,
            subject=subject,
            service_name='Great.gov.uk Search',
            form_url=self.request.path
        )
        response.raise_for_status()
        return super().form_valid(form)

    def get_initial(self):
        return {
            'from_search_query': self.request.GET.get('q', ''),
            'from_search_page': self.request.GET.get('page', '')
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page': self.request.GET.get('page', ''),
            'q': self.request.GET.get('q', '')
        })
        return context


class TestSearchAPIView(TestSearchAPIFeatureFlagMixin, TemplateView):
    """ Due to shifts in the search order provided, we need to
    set up tests for the search order. The challenge is that
    all GDUI does is send an elasticsearch query to the elasticsearch
    database which sits inside the Activity Stream project. Therefore we
    can’t create fixtures in the DB. Also, f we mock the
    database response, then the test doesn’t test anything.

    Another approach would be to test against the staging or
    dev Elasticsearch database... but the results are not guaranteed to
    stay fixed as there are content changes to the data.

    The solution decided on is to feed into the dev database only
    a set of data with an obscure search term (i.e. all have the
    keyword “query123”). The test runs a search for
    that query and tests the sort order of the results. Creating the test feed
    is done by creating a test API within Great Domestic, which is this.
    This is only consumed by the activitystream dev environment.
    """
    template_name = 'test-search-api-pages.json'
