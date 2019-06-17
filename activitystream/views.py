from datetime import datetime
import logging
from requests.exceptions import RequestException

from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from activitystream import helpers, forms
from article.mixins import BreadcrumbsMixin
from core.mixins import SetGA360ValuesMixin

logger = logging.getLogger(__name__)


class SearchView(SetGA360ValuesMixin, TemplateView):
    """ Search results page.

        URL parameters: 'q'    String to be searched
                        'page' Int results page number

        We should use BreadcrumbMixin, however it does not work
    """
    template_name = 'search.html'
    page_type = 'SearchResultsPage'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        results = {}

        query = self.request.GET.get('q', '')
        submitted = self.request.GET.get('submitted', '')
        page = helpers.sanitise_page(self.request.GET.get('page', '1'))
        elasticsearch_query = helpers.format_query(query, page)
        breadcrumbs = [{'url': '/search/', 'label': 'Search'}]

        try:
            response = helpers.search_with_activitystream(elasticsearch_query)

        except RequestException:
            logger.error(
                "Activity Stream connection for "
                "Search failed. Query: '{}'".format(query))

            results = {
                'error_status_code': 500,
                'error_message': "Activity Stream connection failed",
                'query': query,
                'current_page': page,
                'submitted': submitted,
                'breadcrumbs': breadcrumbs
            }

        else:
            if response.status_code != 200:
                results = {
                    'error_message': response.content,
                    'error_status_code': response.status_code,
                    'query': query,
                    'current_page': page,
                    'submitted': submitted,
                    'breadcrumbs': breadcrumbs
                }

            else:
                results = helpers.parse_results(response, query, page, submitted)

        return {**context, **results}


class SearchKeyPagesView(TemplateView):
    """ Returns data on key pages (such as the Get Finance homepage) to
        include in search that are otherwise not provided via other APIs.
    """
    template_name = 'search-key-pages.json'


class SearchFeedbackFormView(BreadcrumbsMixin, FormView):
    template_name = 'search_feedback.html'
    form_class = forms.FeedbackForm

    def get_success_url(self):
        page = self.request.POST['from_search_page']
        query = self.request.POST['from_search_query']
        return f"{reverse_lazy('search')}\
?page={page}&q={query}&submitted=true"

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
            'submitted': self.request.GET.get('submitted', ''),
            'page': self.request.GET.get('page', ''),
            'q': self.request.GET.get('q', '')
        })
        return context
