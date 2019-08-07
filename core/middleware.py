import logging

from directory_api_client.client import api_client
from django.shortcuts import redirect


logger = logging.getLogger(__name__)


class RedirectMiddleware(object):
    def process_request(self, request):
        url = request.path
        if url and url != '':
            response = api_client.redirects.lookup_by_url(source_url=url)

            if response is not None and 'id' in response.keys():
                return redirect(response['target_url'])
        pass
