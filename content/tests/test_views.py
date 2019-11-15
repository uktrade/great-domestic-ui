from unittest import mock

import pytest
from unittest.mock import call, patch
from django.urls import reverse

from core.tests.helpers import create_response
from content.views import MarketsPageView


@pytest.fixture
def mock_get_page():
    stub = patch('directory_cms_client.client.cms_api_client.lookup_by_slug', return_value=create_response())
    yield stub.start()
    stub.stop()


markets_pages = [
    (
        'TopicLandingPage',
        '/markets/'
    ),
    (
        'CountryGuidePage',
        '/markets/australia/'
    )
]


def test_community_article_view(mock_get_page, client):
    mock_get_page.return_value = create_response({
        "meta": {"slug": "foo"},
        "title": "Community article",
        "page_type": "ArticlePage",
        "tree_based_breadcrumbs": [
            {"url": "/advice/", "title": "Topic title"},
            {"url": "/advice/create-an-export-plan/", "title": "List title"},
            {"url": (
                "/advice/create-an-export-plan/how-to-write-an-export-plan/"),
                "title": "How to write an export plan"},
        ]
    })
    url = reverse('community-article')

    response = client.get(url)

    assert response.status_code == 200
    assert mock_get_page.call_count == 1
    assert mock_get_page.call_args == call(
        draft_token=None,
        language_code='en-gb',
        slug='community',
    )


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_get_country_guide_page_attaches_array_lengths(mock_get_page, client):

    page = {
        'title': 'test',
        'page_type': 'CountryGuidePage',
        'tree_based_breadcrumbs': [
            {'url': '/markets/', 'title': 'Markets'},
            {'url': '/markets/japan/', 'title': 'Japan'},
        ],
        'heading': 'Heading',
        'statistics': [
            {'number': '1'},
            {'number': '2', 'heading': 'heading'},
            {'number': None, 'heading': 'no-number-stat'}
        ],
        'accordions': [
            {
                'title': 'title',
                'teaser': 'teaser',
                'statistics': [
                    {'number': '1'},
                    {'number': '2', 'heading': 'heading'},
                    {'number': '3', 'heading': 'heading2'},
                    {'number': None, 'heading': 'no-number-stat'}
                ],
                'subsections': [
                    {'heading': 'heading'},
                    {'heading': 'heading-with-teaser', 'teaser': 'teaser'},
                    {'heading': 'heading-with-teaser-2', 'teaser': 'teaser2'},
                    {'heading': None, 'teaser': 'teaser-without-heading'}
                ],
                'case_study': {'title': 'title', 'image': 'image'}
            }
        ],
        'fact_sheet': {
            'columns': [
                {'title': 'title'},
                {'title': 'title-with-teaser', 'teaser': 'teaser'},
                {'title': None, 'teaser': 'teaser-without-title'}
            ]
        }
    }

    mock_get_page.return_value = create_response(page)

    url = reverse(
        'country-guide',
        kwargs={'slug': 'japan'}
    )
    response = client.get(url)

    view = response.context_data['view']
    assert view.num_of_statistics == 2
    accordions = response.context_data['page']['accordions']
    assert accordions[0]['num_of_statistics'] == 3
    assert accordions[0]['num_of_subsections'] == 3
    assert response.context_data['page']['fact_sheet']['num_of_columns'] == 2


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_get_country_guide_page_viable_accordion(
        mock_get_page,
        client
):
    viable_accordion = {
        'statistics': [],
        'title': 'title',
        'teaser': 'teaser',
        'subsections': [
            {
                'heading': 'heading1'
            },
            {
                'heading': 'heading2'
            }
        ],
        'ctas': [
            {
                'link': 'link1'
            },
            {
                'link': 'link2'
            }
        ],
        'case_study': {'title': 'title', 'image': 'image'}
    }

    page = {
        'title': 'test',
        'page_type': 'CountryGuidePage',
        'tree_based_breadcrumbs': [
            {'url': '/markets/', 'title': 'Markets'},
            {'url': '/markets/japan/', 'title': 'Japan'},
        ],
        'heading': 'Heading',
        'statistics': [],
        'accordions': [viable_accordion],
        'fact_sheet': {
            'columns': []
        }
    }

    mock_get_page.return_value = create_response(page)

    url = reverse(
        'country-guide',
        kwargs={'slug': 'japan'}
    )
    response = client.get(url)

    accordions = response.context_data['page']['accordions']
    assert bool(accordions[0]['is_viable']) is True


non_viable_accordions = [
    {
        'statistics': [],
        'title': '',
        'teaser': 'teaser',
        'subsections': [
            {
                'heading': 'heading1'
            },
            {
                'heading': 'heading2'
            }
        ],
        'case_study': {'title': 'title', 'image': 'image'}
    },
    {
        'statistics': [],
        'title': 'title',
        'teaser': '',
        'subsections': [
            {
                'heading': 'heading1'
            },
            {
                'heading': 'heading2'
            }
        ],
        'case_study': {'title': 'title', 'image': 'image'}
    },
    {
        'statistics': [],
        'title': 'title',
        'teaser': 'teaser',
        'subsections': [
            {
                'heading': 'heading1'
            }
        ],
        'case_study': {'title': 'title', 'image': 'image'}
    },
]


@pytest.mark.parametrize('non_viable_accordion', non_viable_accordions)
@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_get_country_guide_page_non_viable_accordion(
    mock_get_page, non_viable_accordion, client
):
    page = {
        'title': 'test',
        'page_type': 'CountryGuidePage',
        'tree_based_breadcrumbs': [
            {'url': '/markets/', 'title': 'Markets'},
            {'url': '/markets/japan/', 'title': 'Japan'},
        ],
        'heading': 'Heading',
        'statistics': [],
        'accordions': [non_viable_accordion],
        'fact_sheet': {
            'columns': []
        }
    }

    mock_get_page.return_value = create_response(page)

    url = reverse(
        'country-guide',
        kwargs={'slug': 'japan'}
    )
    response = client.get(url)

    accordions = response.context_data['page']['accordions']
    assert bool(accordions[0]['is_viable']) is False


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_get_country_guide_page_viable_case_study(mock_get_page, client):

    page = {
        'title': 'test',
        'page_type': 'CountryGuidePage',
        'tree_based_breadcrumbs': [
            {'url': '/markets/', 'title': 'Markets'},
            {'url': '/markets/japan/', 'title': 'Japan'},
        ],
        'heading': 'Heading',
        'statistics': [],
        'accordions': [{
            'case_study': {
                'title': 'Case study title',
                'image': 'Case study image'
            },
            'statistics': [],
            'title': 'title',
            'teaser': 'teaser',
            'subsections': [],
            'ctas': []
        }],
        'fact_sheet': {
            'columns': []
        }
    }

    mock_get_page.return_value = create_response(page)

    url = reverse(
        'country-guide',
        kwargs={'slug': 'japan'}
    )
    response = client.get(url)

    case_study = response.context_data['page']['accordions'][0]['case_study']
    assert bool(case_study['is_viable']) is True


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_get_country_guide_page_neither_case_study_nor_statistics(
    mock_get_page,
    client
):
    page = {
        'title': 'test',
        'page_type': 'CountryGuidePage',
        'tree_based_breadcrumbs': [
            {'url': '/markets/', 'title': 'Markets'},
            {'url': '/markets/japan/', 'title': 'Japan'},
        ],
        'heading': 'Heading',
        'statistics': [],
        'accordions': [{
            'case_study': {
                'title': '',
                'image': 'Case study image'
            },
            'statistics': [],
            'title': 'title',
            'teaser': 'teaser',
            'subsections': [],
            'ctas': []
        }],
        'fact_sheet': {
            'columns': []
        }
    }

    mock_get_page.return_value = create_response(page)

    url = reverse(
        'country-guide',
        kwargs={'slug': 'japan'}
    )
    response = client.get(url)

    accordion = response.context_data['page']['accordions'][0]
    assert bool(accordion['neither_case_study_nor_statistics']) is True


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@patch('directory_cms_client.client.cms_api_client.lookup_countries_by_tag')
@patch('directory_cms_client.client.cms_api_client.list_industry_tags', mock.MagicMock())
def test_markets_page_filters(mock_countries, mock_page, rf):
    page = {
        'title': 'test',
        'page_type': 'TopicLandingPage',
        'tree_based_breadcrumbs': [
            {'url': '/', 'title': 'great.gov.uk'},
            {'url': '/markets/', 'title': 'Markets'},
        ],
        'child_pages': [{'sorted_title': 'Brazil'}, {'sorted_title': 'China'}, {'sorted_title': 'India'}],
    }

    mock_page.return_value = create_response(page)
    content_list_industry_tags = [{}]
    create_response(content_list_industry_tags)

    filtered_countries = {
        'name': 'Tag name',
        'countries': [{'sorted_title': 'India'}],
    }

    mock_countries.return_value = create_response(filtered_countries)

    request = rf.get('/markets/', {'sector': '1'})
    response = MarketsPageView.as_view()(request, slug='markets')
    response_content = str(response.render().content)

    assert response.status_code == 200
    assert 'Best markets for ' in response_content
    assert response.context_data['pagination_page'].object_list == filtered_countries['countries']


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@patch('directory_cms_client.client.cms_api_client.lookup_countries_by_tag')
@patch('directory_cms_client.client.cms_api_client.list_industry_tags', mock.MagicMock())
def test_markets_page_filters_sort_alphabetically(mock_countries, mock_page, rf):
    page = {
        'title': 'test',
        'page_type': 'TopicLandingPage',
        'tree_based_breadcrumbs': [
            {'url': '/', 'title': 'great.gov.uk'},
            {'url': '/markets/', 'title': 'Markets'},
        ],
        'child_pages': [{'sorted_title': 'India'}, {'sorted_title': 'Japan'}, {'sorted_title': 'Brazil'}],
    }

    sorted_child_pages = sorted(page['child_pages'], key=lambda x: x['sorted_title'])

    mock_page.return_value = create_response(page)
    content_list_industry_tags = [{}]
    create_response(content_list_industry_tags)

    mock_countries.return_value = create_response({})
    request = rf.get('/markets/', {'sector': '2'})
    response = MarketsPageView.as_view()(request, slug='markets')
    response_content = str(response.render().content)

    assert response.status_code == 200
    assert 'Best markets for ' not in response_content
    assert response.context_data['pagination_page'].object_list == sorted_child_pages


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@patch('directory_cms_client.client.cms_api_client.lookup_countries_by_tag')
@patch('directory_cms_client.client.cms_api_client.list_industry_tags', mock.MagicMock())
def test_markets_page_filters_invalid_param(mock_countries, mock_page, rf):
    page = {
        'title': 'test',
        'page_type': 'TopicLandingPage',
        'tree_based_breadcrumbs': [
            {'url': '/', 'title': 'great.gov.uk'},
            {'url': '/markets/', 'title': 'Markets'},
        ],
        'child_pages': [{'sorted_title': 'Brazil'}, {'sorted_title': 'China'}, {'sorted_title': 'India'}],
    }

    mock_page.return_value = create_response(page)
    content_list_industry_tags = [{}]
    create_response(content_list_industry_tags)

    mock_countries.return_value = create_response({})
    request = rf.get('/markets/', {'sector': 'foo'})
    response = MarketsPageView.as_view()(request, slug='markets')
    response_content = str(response.render().content)

    assert response.status_code == 200
    assert 'Best markets for ' not in response_content
    assert response.context_data['pagination_page'].object_list == page['child_pages']


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@patch('directory_cms_client.client.cms_api_client.lookup_countries_by_tag')
@patch('directory_cms_client.client.cms_api_client.list_industry_tags', mock.MagicMock())
def test_markets_page_filters_no_results(mock_countries, mock_page, rf):
    page = {
        'title': 'test',
        'page_type': 'TopicLandingPage',
        'tree_based_breadcrumbs': [
            {'url': '/', 'title': 'great.gov.uk'},
            {'url': '/markets/', 'title': 'Markets'},
        ],
        'child_pages': [{'title': 'India'}, {'title': 'Japan'}, {'title': 'Brazil'}, {'title': 'China'}],
    }

    mock_page.return_value = create_response(page)
    content_list_industry_tags = [{}]
    create_response(content_list_industry_tags)

    filtered_countries = {
        'name': 'Tag name',
        'countries': [],
    }

    mock_countries.return_value = create_response(filtered_countries)
    request = rf.get('/markets/', {'sector': '1'})
    response = MarketsPageView.as_view()(request, slug='markets')
    response_content = str(response.render().content)

    assert response.status_code == 200
    assert 'No results found for ' in response_content
    assert response.context_data['pagination_page'].object_list == filtered_countries['countries']
