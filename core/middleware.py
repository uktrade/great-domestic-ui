import logging

from directory_api_client.client import api_client
from django.shortcuts import redirect
from django.http import HttpResponseNotFound
from django.conf import settings



logger = logging.getLogger(__name__)


class CoreMiddleware(object):

    def process_request(self, request):
        url = request.get_full_path().split('/')[1]
        if url and url != '':
            response = api_client.redirects.lookup_redirect_by_url(source_url=url)
            if response != None and 'id' in response.keys():
                return redirect(response['target_url'], permanent=False)
        pass
