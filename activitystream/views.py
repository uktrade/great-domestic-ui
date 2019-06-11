from datetime import datetime
import logging
from requests.exceptions import RequestException

from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from activitystream import helpers, forms

logger = logging.getLogger(__name__)


class SearchView(TemplateView):
    """ Search results page.

        URL parameters: 'q'    String to be searched
                        'page' Int results page number
    """
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('q', '')
        page = helpers.sanitise_page(self.request.GET.get('page', '1'))
        elasticsearch_query = helpers.format_query(query, page)

        try:
            response = helpers.search_with_activitystream(elasticsearch_query)
        except RequestException:
            logger.error(
                "Activity Stream connection for"
                "Search failed. Query: '{}'".format(query))
            return {
                'error_status_code': 500,
                'error_message': "Activity Stream connection failed",
                'query': query,
                'current_page': page
            }
        else:
            if response.status_code != 200:
                return {
                    'error_message': response.content,
                    'error_status_code': response.status_code,
                    'query': query,
                    'current_page': page
                }
            else:
                return helpers.parse_results(response, query, page)


class SearchKeyPagesView(TemplateView):
    """ Returns data on key pages (such as the Get Finance homepage) to
        include in search that are otherwise not provided via other APIs.
    """
    template_name = 'search-key-pages.json'


class SearchFeedbackFormView(FormView):
    template_name = 'search_feedback.html'
    form_class = forms.FeedbackForm

    def get_success_url(self):
        page = self.request.POST['from_search_page']
        query = self.request.POST['from_search_query']
        return f"{reverse_lazy('search-feedback-received')}\
?page={page}&query={query}"

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


class SearchFeedbackReceivedView(TemplateView):
    template_name = 'search_feedback_received.html'

    def get_context_data(self, **kwargs):
        return {
            'page': self.request.GET.get('page', ''),
            'query': self.request.GET.get('query', '')
        }
