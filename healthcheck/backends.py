from health_check.backends import BaseHealthCheckBackend
from health_check.exceptions import ServiceReturnedUnexpectedResult

from django.urls import reverse_lazy
from django.test import Client as TestClient


class SearchSortBackend(BaseHealthCheckBackend):

    def check_status(self):

        client = TestClient()
        response = client.get(reverse_lazy('search'), data={'q': 'qwerty123'})

        ordering_success = False
        if response.status_code == 200:
            results = response.context_data['results']
            if (len(results) == 4) and \
               (results[0]["type"] == "Service") and \
               (results[-1]["type"] == "Export opportunity"):
                    ordering_success = True

        if not ordering_success:
            raise ServiceReturnedUnexpectedResult(
                'Search sort ordering via Activity Stream failed'
            )

        return True
