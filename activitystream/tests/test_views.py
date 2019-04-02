import json
import requests
import pytest

from unittest.mock import patch, Mock
from django.core.urlresolvers import reverse

def test_search_view_feature_flag(client, settings):
    settings.FEATURE_FLAGS['SEARCH_ON'] = False

    response = client.get(reverse('search'), data={'q': 'services'})

    assert response.status_code == 404


def test_search_view(client):
    """ We mock the call to ActivityStream """
    with patch('activitystream.helpers.search_with_activitystream') as search:
        mock_results = json.dumps({
            'took': 17,
            'timed_out': False,
            '_shards': {
                'total': 4,
                'successful': 4,
                'skipped': 0,
                'failed': 0
            },
            'hits': {
                'total': 5,
                'max_score': 0.2876821,
                'hits': [{
                    '_index': 'objects__feed_id_first_feed__date_2019',
                    '_type': '_doc',
                    '_id': 'dit:exportOpportunities:Opportunity:2',
                    '_score': 0.2876821,
                    '_source': {
                        'type': 'Opportunities',
                        'title': 'France - Data analysis services',
                        'content':
                        'The purpose of this contract is to analyze...',
                        'url': 'www.great.gov.uk/opportunities/1'
                    }
                }, {
                    '_index': 'objects__feed_id_first_feed__date_2019',
                    '_type': '_doc',
                    '_id': 'dit:exportOpportunities:Opportunity:2',
                    '_score': 0.18232156,
                    '_source': {
                        'type': 'Opportunities',
                        'title': 'Germany - snow clearing',
                        'content':
                        'Winter services for the properties1) Former...',
                        'url': 'www.great.gov.uk/opportunities/2'
                    }
                }]
            }
        })
        search.return_value = Mock(status_code=200, content=mock_results)

        response = client.get(reverse('search'), data={'q': 'services'})
        context = response.context_data

        assert response.status_code == 200
        assert context['results'] == [
                {
                  "type": "Opportunities",
                  "title": "France - Data analysis services",
                  "content": "The purpose of this contract is to analyze...",
                  "url": "www.great.gov.uk/opportunities/1"
                },
                {
                  "type": "Opportunities",
                  "title": "Germany - snow clearing",
                  "content": "Winter services for the properties1) Former...",
                  "url": "www.great.gov.uk/opportunities/2"
                }
            ]

        """ What if there are no results? """
        search.return_value = Mock(
            status_code=200,
            content=json.dumps({
                'took': 17,
                'timed_out': False,
                '_shards': {
                    'total': 4,
                    'successful': 4,
                    'skipped': 0,
                    'failed': 0
                },
                'hits': {
                    'total': 0,
                    'hits': []
                }
            })
        )

        response = client.get(reverse('search'), data={'q': 'services'})
        context = response.context_data

        assert response.status_code == 200
        assert context['results'] == []

        """ What if ActivitySteam sends an error? """
        search.return_value = Mock(status_code=500,
                                   content="[service overloaded]")

        response = client.get(reverse('search'), data={'q': 'services'})
        context = response.context_data

        assert response.status_code == 200
        # This can be handled on the front end as we wish
        assert context['error_message'] == "[service overloaded]"
        assert context['error_status_code'] == 500

        """ What if ActivitySteam is down? """
        search.side_effect = requests.exceptions.ConnectionError

        response = client.get(reverse('search'), data={'q': 'services'})
        context = response.context_data

        assert response.status_code == 200
        # This can be handled on the front end as we wish
        assert context['error_message'] == "Activity Stream connection failed"
        assert context['error_status_code'] == 500


def test_search_key_pages_view(client):
    response = client.get(reverse('search-key-pages'))
    feed_parsed = json.loads(response.content)
    assert feed_parsed["orderedItems"][0]["object"]["name"] == \
        "Get finance - Homepage"

