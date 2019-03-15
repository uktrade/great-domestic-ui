import json
from unittest.mock import patch, Mock, PropertyMock

import pytest
import requests
from requests.exceptions import ConnectionError
import requests_mock

from django.shortcuts import Http404
from django.urls import reverse

from core import helpers
from core.management.commands.download_geolocation_data import (
    GeolocationLocalFileArchive
)
import core.tests.helpers


def test_build_twitter_link(rf):
    request = rf.get('/')
    actual = helpers.build_twitter_link(
        request=request,
        title='Do research first',
    )

    assert actual == (
        'https://twitter.com/intent/tweet'
        '?text=Export%20Readiness%20-%20Do%20research%20first%20'
        'http://testserver/'
    )


def test_build_facebook_link(rf):
    request = rf.get('/')
    actual = helpers.build_facebook_link(
        request=request,
        title='Do research first',
    )
    assert actual == (
        'https://www.facebook.com/share.php?u=http://testserver/'
    )


def test_build_linkedin_link(rf):
    request = rf.get('/')
    actual = helpers.build_linkedin_link(
        request=request,
        title='Do research first',
    )

    assert actual == (
        'https://www.linkedin.com/shareArticle?mini=true&'
        'url=http://testserver/&'
        'title=Export%20Readiness%20-%20Do%20research%20first%20'
        '&source=LinkedIn'
    )


def test_build_email_link(rf):
    request = rf.get('/')
    actual = helpers.build_email_link(
        request=request,
        title='Do research first',
    )

    assert actual == (
        'mailto:?body=http://testserver/'
        '&subject=Export%20Readiness%20-%20Do%20research%20first%20'
    )


@pytest.mark.parametrize('status_code,exception', (
    (400, requests.exceptions.HTTPError),
    (404, Http404),
    (500, requests.exceptions.HTTPError),
))
def test_handle_cms_response_error(status_code, exception):
    response = core.tests.helpers.create_response(status_code=status_code)
    with pytest.raises(exception):
        helpers.handle_cms_response(response)


def test_handle_cms_response_ok():
    response = core.tests.helpers.create_response(
        status_code=200, json_body={'field': 'value'}
    )

    assert helpers.handle_cms_response(response) == {'field': 'value'}


@pytest.mark.parametrize('status_code,exception', (
    (400, requests.exceptions.HTTPError),
    (500, requests.exceptions.HTTPError),
))
def test_handle_cms_response_allow_404_error(status_code, exception):
    response = core.tests.helpers.create_response(status_code=status_code)
    with pytest.raises(exception):
        helpers.handle_cms_response_allow_404(response)


def test_handle_cms_response_allow_404_not_found():
    response = core.tests.helpers.create_response(status_code=404)
    assert helpers.handle_cms_response_allow_404(response) == {}


def test_handle_cms_response_allow_404_ok():
    response = core.tests.helpers.create_response(
        status_code=200, json_body={'field': 'value'}
    )
    assert helpers.handle_cms_response_allow_404(response) == {
        'field': 'value'}


@patch('core.helpers.get_client_ip', Mock(return_value=(None, False)))
def test_geolocation_redirector_unroutable(rf):
    request = rf.get('/')
    redirector = helpers.GeoLocationRedirector(request)

    assert redirector.should_redirect is False


@patch('core.helpers.get_client_ip', Mock(return_value=('8.8.8.8', True)))
def test_geolocation_redirector_cookie_set(rf):
    request = rf.get('/')
    request.COOKIES[helpers.GeoLocationRedirector.COOKIE_NAME] = True
    redirector = helpers.GeoLocationRedirector(request)

    assert redirector.should_redirect is False


@patch('core.helpers.get_client_ip', Mock(return_value=('8.8.8.8', True)))
def test_geolocation_redirector_language_param(rf):
    request = rf.get('/', {'lang': 'en-gb'})
    redirector = helpers.GeoLocationRedirector(request)

    assert redirector.should_redirect is False


@patch('core.helpers.get_client_ip', Mock(return_value=('8.8.8.8', True)))
@patch(
    'core.helpers.GeoLocationRedirector.country_code',
    PropertyMock(return_value=None)
)
def test_geolocation_redirector_unknown_country(rf):
    request = rf.get('/', {'lang': 'en-gb'})
    redirector = helpers.GeoLocationRedirector(request)

    assert redirector.should_redirect is False


@patch('core.helpers.get_client_ip', Mock(return_value=('8.8.8.8', True)))
@patch(
    'core.helpers.GeoLocationRedirector.country_code',
    new_callable=PropertyMock
)
@pytest.mark.parametrize(
    'country_code', helpers.GeoLocationRedirector.DOMESTIC_COUNTRY_CODES
)
def test_geolocation_redirector_is_domestic(
    mock_country_code, rf, country_code
):
    mock_country_code.return_value = country_code

    request = rf.get('/', {'lang': 'en-gb'})
    redirector = helpers.GeoLocationRedirector(request)

    assert redirector.should_redirect is False


@patch('core.helpers.get_client_ip', Mock(return_value=('8.8.8.8', True)))
@patch(
    'core.helpers.GeoLocationRedirector.country_code',
    new_callable=PropertyMock
)
@pytest.mark.parametrize(
    'country_code', helpers.GeoLocationRedirector.COUNTRY_TO_LANGUAGE_MAP
)
def test_geolocation_redirector_is_international(
    mock_country_code, rf, country_code
):
    mock_country_code.return_value = country_code

    request = rf.get('/')
    redirector = helpers.GeoLocationRedirector(request)

    assert redirector.should_redirect is True


@pytest.mark.parametrize('ip_address,language', (
    ('221.194.47.204', 'zh-hans'),
    ('144.76.204.44', 'de'),
    ('195.12.50.155', 'es'),
    ('110.50.243.6', 'ja'),
))
def test_geolocation_end_to_end(rf, ip_address, language, settings):
    request = rf.get('/', {'a': 'b'}, REMOTE_ADDR=ip_address)

    archive = GeolocationLocalFileArchive()
    archive.decompress(
        file_name=settings.GEOIP_COUNTRY,
        destination=settings.GEOIP_PATH
    )

    redirector = helpers.GeoLocationRedirector(request)

    assert redirector.should_redirect is True
    url, querysrtring = redirector.get_response().url.split('?')
    assert url == reverse('landing-page-international')
    assert 'lang=' + language in querysrtring
    assert 'a=b' in querysrtring


def test_search():
    with requests_mock.mock() as mock:
        mock.get(
            'https://api.companieshouse.gov.uk/search/companies',
            status_code=200,
        )
        response = helpers.CompaniesHouseClient.search(term='green')
        assert response.status_code == 200

    request = mock.request_history[0]

    assert request.query == 'q=green'


def test_search_unauthorized():
    with requests_mock.mock() as mock:
        mock.get(
            'https://api.companieshouse.gov.uk/search/companies',
            status_code=401,
        )
        with pytest.raises(requests.HTTPError):
            helpers.CompaniesHouseClient.search(term='green')


''' -- Search helpers -- '''


@pytest.mark.parametrize('query,safe_output', (
    ("SELECT * FROM Users WHERE Username='1' OR \
'1' = '1' AND Password='1' OR '1' = '1' ",
     "SELECT FROM Users WHERE Username '1' OR \
'1' '1' AND Password '1' OR '1' '1'"),
    ("$password = 1' or '1' = '1", "password 1' or '1' '1"),
    ("'search=keyword'and'1'='1'", "'search keyword'and'1' '1'"),
    ("innocent search'dropdb();", "innocent search'dropdb"),
    ("{\"script\": \"ctx._source.viewings += 1}\"",
        "script ctx source viewings 1")
))
def test_sanitise_query(query, safe_output):
    assert helpers.sanitise_query(query) == safe_output


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


def test_parse_results():
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
            'total': 50,
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
    assert helpers.parse_results(response, "services", 2) == {
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
       'total_results': 50,
       'current_page': 2,
       'total_pages': 5,
       'previous_page': 1,
       'next_page': 3,
       'prev_pages': [1],
       'next_pages': [3, 4, 5],
       'show_first_page': False,
       'show_last_page': False
    }


def test_format_query():
    assert helpers.format_query("services", 2) == json.dumps({
        "query": {
          "bool": {
              "should": [
                  {"match": {"id": "services"}},
                  {"match": {"name": "services"}},
                  {"match": {"content": "services"}},
                  {"match": {"type": "services"}}
              ]
          }
        },
        "from": 10,
        "size": 10
    })


def test_search_with_activitystream():
    ''' Simply check that it doesn't expload,
        and instead raises correct no-connection error '''
    with pytest.raises(ConnectionError):
        helpers.search_with_activitystream(
            helpers.format_query("Test", 1)
        )
