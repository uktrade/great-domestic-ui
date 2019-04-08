import json
import pytest

from requests.exceptions import ConnectionError
from unittest.mock import Mock

from activitystream import helpers


@pytest.mark.parametrize('page,safe_output', (
    ("2", 2),
    ("-1", 1),
    ("abc", 1),
    ("$password = 1' or '1' = '1", 1),
    ("'search=keyword'and'1'='1'", 1),
    ("innocent search'dropdb();", 1),
    ("{\"script\": \"ctx._source.viewings += 1}\"", 1)
))
def test_sanitise_page(page, safe_output):
    assert helpers.sanitise_page(page) == safe_output


@pytest.mark.parametrize(
    'page,prev_pages,next_pages,show_first_page,\
show_last_page,first_item_number,last_item_number', (
        (2, [1], [3, 4, 5], False, True, 11, 20),
        (9, [6, 7, 8], [10], True, False, 81, 90),
    )
)
def test_parse_results(page, prev_pages,
                       next_pages, show_first_page,
                       show_last_page, first_item_number,
                       last_item_number):
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
            'total': 100,
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
    response = Mock(status=200, content=mock_results)
    assert helpers.parse_results(response, "services", page) == {
       'query': "services",
       'results': [{
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
        }],
       'total_results': 100,
       'current_page': page,
       'total_pages': 10,
       'previous_page': page-1,
       'next_page': page+1,
       'prev_pages': prev_pages,
       'next_pages': next_pages,
       'show_first_page': show_first_page,
       'show_last_page': show_last_page,
       'first_item_number': first_item_number,
       'last_item_number': last_item_number
    }


def test_format_query():
    assert helpers.format_query("services", 2) == json.dumps({
        'query': {
          'bool': {
                'should': [
                    {
                        'match': {
                            'name': {
                                'query': 'services',
                                'minimum_should_match': '2<75%'
                            }
                        }
                    },
                    {
                        'match': {
                            'content': {
                                'query': 'services',
                                'minimum_should_match': '2<75%'
                            }
                        }
                    },
                    {'match': {'keywords': 'services'}},
                    {'match': {'type': 'services'}}, {
                        'match': {
                            'name': {
                                'query': 'Guidance\
 on how to prepare for EU Exit', 'boost': 20
                                }
                            }
                    }
                ]
            }
        },
        'from': 10,
        'size': 10,
        'indices_boost': [
            {'objects__feed_id_key_pages*': 10},
            {'objects__feed_id_export_opportunities*': 0.1},
            {'objects*': 1}
        ]
    })


def test_search_with_activitystream():
    """ Simply check that it doesn't expload,
        and instead raises correct no-connection error
    """
    with pytest.raises(ConnectionError):
        helpers.search_with_activitystream(
            helpers.format_query("Test", 1)
        )
