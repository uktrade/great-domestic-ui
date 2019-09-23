from unittest.mock import patch, Mock

from healthcheck import backends


@patch('django.test.Client.get',
       Mock(return_value=Mock(status_code=500)))
def test_search_sort_not_ok():
    backend = backends.SearchSortBackend()
    backend.run_check()

    assert backend.pretty_status() == \
        'unexpected result: Search sort ordering via Activity Stream failed'


@patch('django.test.Client.get',
       Mock(return_value=Mock(status_code=200, context_data={"results": [
                {"type": "Service"}, {}, {}, {"type": "Export opportunity"}
            ]})))
def test_search_sort_ok():
    backend = backends.SearchSortBackend()
    backend.run_check()

    assert backend.pretty_status() == 'working'
