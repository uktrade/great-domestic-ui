import json
import requests
from math import ceil

from django.conf import settings
from mohawk import Sender
from raven.contrib.django.raven_compat.models import client

from activitystream import serializers

RESULTS_PER_PAGE = 10


def sanitise_page(page):
    try:
        return int(page) if int(page) > 0 else 1
    except ValueError:
        return 1


def parse_results(response, query, page):
    current_page = int(page)

    content = json.loads(response.content)

    if 'error' in content:
        results = []
        total_results = 0
        total_pages = 1
        client.captureMessage(
            f"There was an error in /search: {content['error']}"
        )
    else:
        results = serializers.parse_search_results(content)
        total_results = content['hits']['total']
        total_pages = ceil(total_results/float(RESULTS_PER_PAGE))

    prev_pages = list(range(1, current_page))[-3:]
    if (len(prev_pages) > 0) and (prev_pages[0] > 2):
        show_first_page = True
    else:
        show_first_page = False

    next_pages = list(range(current_page + 1, total_pages + 1))[:3]
    if (len(next_pages) > 0) and (next_pages[-1] + 1 < total_pages):
        show_last_page = True
    else:
        show_last_page = False

    first_item_number = ((current_page-1)*RESULTS_PER_PAGE) + 1
    if current_page == total_pages:
        last_item_number = total_results
    else:
        last_item_number = (current_page)*RESULTS_PER_PAGE

    return {
       'query': query,
       'results': results,
       'total_results': total_results,
       'current_page': current_page,
       'total_pages': total_pages,
       'previous_page': current_page - 1,
       'next_page': current_page + 1,
       'prev_pages': prev_pages,
       'next_pages': next_pages,
       'show_first_page': show_first_page,
       'show_last_page': show_last_page,
       'first_item_number': first_item_number,
       'last_item_number': last_item_number
    }


def format_query(query, page):
    """ formats query for ElasticSearch
    Note: ActivityStream not yet configured to recieve pagination,
    will be corrected shortly. Hence commented-out lines.
    """
    from_result = (page - 1) * RESULTS_PER_PAGE
    return json.dumps({
        'query': {
            'bool': {
                'must': {
                    'bool': {
                        'should': [
                            {
                                'match': {
                                    'name': {
                                        'query': query,
                                        'minimum_should_match': '2<75%'
                                    }
                                }
                            },
                            {
                                'match': {
                                    'content': {
                                        'query': query,
                                        'minimum_should_match': '2<75%'
                                    }
                                }
                            },
                            {'match': {'keywords': query}},
                            {'match': {'type': query}}
                        ]
                    }
                },
                'should': [{
                    'match': {
                        'boost': {
                            'query': query,
                            'boost': 20
                        }
                    }
                }]
            }
        },
        'from': from_result,
        'size': RESULTS_PER_PAGE,
        'indices_boost': [
            {'objects__feed_id_key_pages*': 10},
            {'objects__feed_id_export_opportunities*': 0.1},
            {'objects*': 1}
        ]
    })


def search_with_activitystream(query):
    """ Searches ActivityStream services with given Elasticsearch query.
        Note that this must be at root level in SearchView class to
        enable it to be mocked in tests.
    """
    request = requests.Request(
        method="GET",
        url=settings.ACTIVITY_STREAM_API_URL,
        data=query).prepare()

    auth = Sender(
        {
            'id': settings.ACTIVITY_STREAM_API_ACCESS_KEY,
            'key': settings.ACTIVITY_STREAM_API_SECRET_KEY,
            'algorithm': 'sha256'
        },
        settings.ACTIVITY_STREAM_API_URL,
        "GET",
        content=query,
        content_type='application/json',
    ).request_header

    request.headers.update({
        'X-Forwarded-Proto': 'https',
        'X-Forwarded-For': settings.ACTIVITY_STREAM_API_IP_WHITELIST,
        'Authorization': auth,
        'Content-Type': 'application/json'
    })

    return requests.Session().send(request)
