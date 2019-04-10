import pytest
from unittest.mock import call, patch
from django.urls import reverse

from core.tests.helpers import create_response


@pytest.fixture
def mock_get_page():
    stub = patch(
        'directory_cms_client.client.cms_api_client.lookup_by_slug',
        return_value=create_response(status_code=200)
    )
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


@pytest.mark.parametrize('page_type,url', markets_pages)
def test_markets_pages_404_when_feature_off(
    mock_get_page, page_type, url, client, settings
):
    settings.FEATURE_FLAGS['MARKETS_PAGES_ON'] = False

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body={
            'page_type': page_type,
        }
    )

    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.parametrize('page_type,url', markets_pages)
def test_markets_pages_200_when_feature_on(
    mock_get_page, page_type, url, client, settings
):
    settings.FEATURE_FLAGS['MARKETS_PAGES_ON'] = True

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body={
            'page_type': page_type,
            'heading': 'Heading',
            'statistics': [],
            'accordions': [],
            'fact_sheet': {'columns': []},
            'child_pages': []
        }
    )

    response = client.get(url)

    assert response.status_code == 200


def test_news_list_page_feature_flag_off(client, settings):
    settings.FEATURE_FLAGS['NEWS_SECTION_ON'] = False

    url = reverse('eu-exit-news-list')

    response = client.get(url)

    assert response.status_code == 404


def test_breadcrumbs_mixin(mock_get_page, client, settings):
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = False

    url = reverse('create-an-export-plan-article', kwargs={'slug': 'foo'})

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body={
            'page_type': 'ArticlePage'
        }
    )
    response = client.get(url)

    breadcrumbs = response.context_data['breadcrumbs']
    assert breadcrumbs == [
        {
            'url': '/advice/',
            'label': 'Advice'
        },
        {
            'url': '/advice/create-an-export-plan/',
            'label': 'Create an export plan'
        },
        {
            'url': '/advice/create-an-export-plan/foo/',
            'label': 'Foo'
        },
    ]


def test_community_article_view(mock_get_page, client):
    mock_get_page.return_value = create_response(200, {
        "meta": {"slug": "foo"},
        "page_type": "ArticlePage",
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
                'ctas': [
                    {'title': 'title', 'link': 'link'},
                    {'title': 'title no link', 'link': None},
                    {'title': None, 'link': 'link-but-no-title'}
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

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=page
    )

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
    assert accordions[0]['num_of_ctas'] == 2
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
        'heading': 'Heading',
        'statistics': [],
        'accordions': [viable_accordion],
        'fact_sheet': {
            'columns': []
        }
    }

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=page
    )

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
        'ctas': [
            {
                'link': 'link1'
            },
            {
                'link': 'link2'
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
        'ctas': [
            {
                'link': 'link1'
            },
            {
                'link': 'link2'
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
        'ctas': [
            {
                'link': 'link1'
            },
            {
                'link': 'link2'
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
            },
            {
                'heading': 'heading2'
            }
        ],
        'ctas': [
            {
                'link': 'link1'
            }
        ],
        'case_study': {'title': 'title', 'image': 'image'}
    }
]


@pytest.mark.parametrize('non_viable_accordion', non_viable_accordions)
@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_get_country_guide_page_non_viable_accordion(
    mock_get_page,
    non_viable_accordion,
    client
):
    page = {
        'title': 'test',
        'page_type': 'CountryGuidePage',
        'heading': 'Heading',
        'statistics': [],
        'accordions': [non_viable_accordion],
        'fact_sheet': {
            'columns': []
        }
    }

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=page
    )

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

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=page
    )

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

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=page
    )

    url = reverse(
        'country-guide',
        kwargs={'slug': 'japan'}
    )
    response = client.get(url)

    accordion = response.context_data['page']['accordions'][0]
    assert bool(accordion['neither_case_study_nor_statistics']) is True


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_get_markets_page_renames_heading_to_landing_page_title(
    mock_get_page, client
):
    page = {
        'title': 'test',
        'page_type': 'TopicLandingPage',
        'child_pages': [
            {
                'heading': 'heading'
            }
        ]
    }

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=page
    )

    url = reverse('markets')
    response = client.get(url)

    child_page = response.context_data['page']['child_pages'][0]
    assert child_page['landing_page_title'] == 'heading'
