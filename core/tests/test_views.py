from unittest import mock
from unittest.mock import call, patch

import requests

from django.urls import reverse
from django.conf import settings
from django.views.generic import TemplateView

import pytest
import requests_mock
from rest_framework import status

from core import views
from core.tests.helpers import create_response

from directory_constants import slugs, urls


def test_exopps_redirect(client):
    url = reverse('export-opportunities')
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == settings.SERVICES_EXOPPS_ACTUAL


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@patch('directory_cms_client.client.cms_api_client.list_industry_tags')
def test_top_sectors_returned(mock_industries, mock_get_page, client):

    page = {
        'title': 'great.gov.uk',
        'page_type': 'HomePage',
        'news_title': 'News',
        'news_description': '<p>Lorem ipsum</p>',
        'articles': [
            {'article_title': 'News article 1'},
            {'article_title': 'News article 2'},
        ],
        'guidance': [
            {'title': 'Guidance 1'},
            {'title': 'Guidance 2'},
        ],
        'tree_based_breadcrumbs': [
            {'url': '/', 'title': 'great.gov.uk'},
        ]
    }
    mock_get_page.return_value = create_response(page)
    content_list_industry_tags = [
        {'id': 1, 'name': 'Agri-technology', 'icon': None, 'pages_count': 3},
        {'id': 2, 'name': 'Agri-technology1', 'icon': None, 'pages_count': 6},
        {'id': 3, 'name': 'Agri-technology2', 'icon': None, 'pages_count': 8},
        {'id': 4, 'name': 'Agri-technology3', 'icon': None, 'pages_count': 6},
        {'id': 5, 'name': 'Agri-technology4', 'icon': None, 'pages_count': 1},
        {'id': 6, 'name': 'Agri-technology5', 'icon': None, 'pages_count': 0},
        {'id': 7, 'name': 'Agri-technology6', 'icon': None, 'pages_count': 3},
        {'id': 8, 'name': 'Agri-technology', 'icon': None, 'pages_count': 2},
        {'id': 9, 'name': 'Agri-technology', 'icon': None, 'pages_count': 1},
    ]
    mock_industries.return_value = create_response(content_list_industry_tags)

    url = reverse('landing-page')
    response = client.get(url)

    assert len(response.context_data['sector_list']) == 6


def test_sitemaps(client):
    url = reverse('sitemap')

    response = client.get(url)

    assert response.status_code == 200


def test_robots(client):
    url = reverse('robots')

    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.parametrize(
    'view,expected_template',
    (
        (
            'not-found',
            '404.html'
        ),
    )
)
def test_templates(view, expected_template, client):
    url = reverse(view)

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [expected_template]


@pytest.mark.parametrize(
    'view,expected_template',
    (
        (
            'terms-and-conditions',
            'core/info_page.html'
        ),
    )
)
@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_terms_conditions_cms(mock_get_t_and_c_page, view, expected_template, client):
    url = reverse(view)
    page = {
        'title': 'the page',
        'meta': {'languages': ['en-gb']},
        'page_type': 'TermsAndConditionsPage',
        'tree_based_breadcrumbs': [
            {'url': '/terms-and-conditions/', 'title': 'the page'},
        ]
    }
    mock_get_t_and_c_page.return_value = create_response(page)
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [expected_template]


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_privacy_cookies_cms(mock_get_page, client):
    expected_template = 'core/info_page.html'
    url = reverse('privacy-and-cookies')
    page = {
        'title': 'the page',
        'industries': [{'title': 'good 1'}],
        'meta': {'languages': ['en-gb']},
        'page_type': 'PrivacyAndCookiesPage',
        'tree_based_breadcrumbs': [
            {'url': '/privacy-and-cookies/', 'title': 'the page'},
        ]
    }
    mock_get_page.return_value = create_response(page)
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [expected_template]


@pytest.mark.parametrize(
    'view,expected_template',
    (
        (
            'accessibility-statement',
            'core/info_page.html'
        ),
    )
)
@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_accessibility_statement_cms(
    mock_get_page, view, expected_template, client
):
    url = reverse(view)
    page = {
        'title': 'the page',
        'meta': {'languages': ['en-gb']},
        'page_type': 'PrivacyAndCookiesPage',
        'tree_based_breadcrumbs': [
            {'url': '/accessibility-statement/', 'title': 'the page'},
        ]
    }
    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=page
    )
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [expected_template]


@pytest.mark.parametrize('method,expected', (
    ('get', '"b013a413446c5dddaf341792c63a88c4"'),
    ('post', None),
    ('patch', None),
    ('put', None),
    ('delete', None),
    ('head', None),
    ('options', None),
))
def test_set_etag_mixin(rf, method, expected):
    class MyView(views.SetEtagMixin, TemplateView):

        template_name = 'robots.txt'

        def post(self, *args, **kwargs):
            return super().get(*args, **kwargs)

        def patch(self, *args, **kwargs):
            return super().get(*args, **kwargs)

        def put(self, *args, **kwargs):
            return super().get(*args, **kwargs)

        def delete(self, *args, **kwargs):
            return super().get(*args, **kwargs)

        def head(self, *args, **kwargs):
            return super().get(*args, **kwargs)

        def options(self, *args, **kwargs):
            return super().get(*args, **kwargs)

    request = getattr(rf, method)('/')
    request.user = None
    view = MyView.as_view()
    response = view(request)

    response.render()
    assert response.get('Etag') == expected


@pytest.mark.parametrize('view_class', views.SetEtagMixin.__subclasses__())
def test_cached_views_not_dynamic(rf, view_class):
    # exception will be raised if the views perform http request, which are an
    # indicator that the views rely on dynamic data.
    with requests_mock.mock():
        view = view_class.as_view()
        request = rf.get('/')
        request.LANGUAGE_CODE = 'en-gb'
        # highlights if the view tries to interact with the session, which is
        # also an indicator that the view relies on dynamic data.
        request.session = None
        response = view(request)
        assert response.status_code == 200


cms_urls_slugs = (
    (
        reverse('privacy-and-cookies'),
        slugs.GREAT_PRIVACY_AND_COOKIES,
    ),
    (
        reverse('terms-and-conditions'),
        slugs.GREAT_TERMS_AND_CONDITIONS,
    ),
    (
        reverse('accessibility-statement'),
        slugs.GREAT_ACCESSIBILITY_STATEMENT,
    ),
)


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@pytest.mark.parametrize('url,slug', cms_urls_slugs)
def test_cms_pages_cms_client_params(mock_get, client, url, slug):
    mock_get.return_value = create_response({
        'title': 'The page',
        'page_type': 'GenericPage',
        'meta': {'languages': (['en-gb', 'English'])},
        'tree_based_breadcrumbs': [
            {'title': 'The page', 'url': '/'}
        ],
    })

    response = client.get(url, {'draft_token': '123'})

    assert response.status_code == 200
    assert mock_get.call_count == 1
    assert mock_get.call_args == call(
        slug=slug,
        draft_token='123',
        language_code='en-gb'
    )


cms_urls = (
    reverse('privacy-and-cookies'),
    reverse('terms-and-conditions'),
    reverse('accessibility-statement'),
)


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@pytest.mark.parametrize('url', cms_urls)
def test_cms_pages_cms_page_404(mock_get, client, url):
    mock_get.return_value = create_response(status_code=404)

    response = client.get(url)

    assert response.status_code == 404


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_performance_dashboard_cms(mock_get_page, settings, client):
    settings.FEATURE_FLAGS['PERFORMANCE_DASHBOARD_ON'] = True
    url = reverse('performance-dashboard')
    page = {
        'title': 'Performance dashboard',
        'heading': 'great.gov.uk',
        'description': 'Lorem ipsum dolor sit amet.',
        'page_type': 'PerformanceDashboardPage',
        'tree_based_breadcrumbs': [
            {'title': 'The page', 'url': '/'}
        ],
    }
    mock_get_page.return_value = create_response(page)
    response = client.get(url)

    assert page['title'] in str(response.content)
    assert page['heading'] in str(response.content)
    assert page['description'] in str(response.content)

    assert response.status_code == 200
    assert response.template_name == ['core/performance_dashboard.html']


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_privacy_cookies_subpage(mock_get_page, client):
    url = reverse(
        'privacy-and-cookies-subpage',
        kwargs={'slug': 'fair-processing-notice-zendesk'}
    )
    page = {
        'title': 'Fair Processing Notice Zendesk',
        'body': 'Lorem ipsum dolor sit amet.',
        'page_type': 'PrivacyAndCookiesPage',
        'tree_based_breadcrumbs': [
            {'title': 'The page', 'url': '/'}
        ],
    }
    mock_get_page.return_value = create_response(page)
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['core/info_page.html']

    assert page['title'] in str(response.content)
    assert page['body'] in str(response.content)


@pytest.mark.parametrize('view_name', ['triage-start', 'custom-page'])
@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_triage_views(mock_get_page, view_name, client):
    mock_get_page.return_value = create_response({
        'title': 'Advice',
        'page_type': 'TopicLandingPage',
    })

    url = reverse(view_name)
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.template_name == ['core/service_no_longer_available.html']


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_triage_wizard_view(mock_get_page, client):
    mock_get_page.return_value = create_response({
        'title': 'Advice',
        'page_type': 'TopicLandingPage',
    })
    url = reverse('triage-wizard', kwargs={'step': 'foo'})
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.template_name == ['core/service_no_longer_available.html']


def test_companies_house_search_validation_error(client, settings):
    settings.FEATURE_FLAGS['INTERNAL_CH_ON'] = False

    url = reverse('api-internal-companies-house-search')
    response = client.get(url)  # notice absense of `term`

    assert response.status_code == 400


@patch('core.helpers.CompaniesHouseClient.search')
def test_companies_house_search_api_error(mock_search, client, settings):
    settings.FEATURE_FLAGS['INTERNAL_CH_ON'] = False

    mock_search.return_value = create_response(status_code=400)
    url = reverse('api-internal-companies-house-search')

    with pytest.raises(requests.HTTPError):
        client.get(url, data={'term': 'thing'})


@patch('core.helpers.CompaniesHouseClient.search')
def test_companies_house_search_api_success(mock_search, client, settings):
    settings.FEATURE_FLAGS['INTERNAL_CH_ON'] = False

    mock_search.return_value = create_response({'items': [{'name': 'Smashing corp'}]})
    url = reverse('api-internal-companies-house-search')

    response = client.get(url, data={'term': 'thing'})

    assert response.status_code == 200
    assert response.content == b'[{"name": "Smashing corp"}]'


@patch('core.helpers.ch_search_api_client.company.search_companies')
def test_companies_house_search_internal(mock_search_companies, client, settings):
    settings.FEATURE_FLAGS['INTERNAL_CH_ON'] = True

    mock_search_companies.return_value = create_response({'items': [{'name': 'Smashing corp'}]})
    url = reverse('api-internal-companies-house-search')

    response = client.get(url, data={'term': 'thing'})

    assert response.status_code == 200
    assert response.content == b'[{"name": "Smashing corp"}]'


def test_international_trade_redirect_home(client):
    url = reverse('international-trade-home')
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == urls.international.TRADE_HOME


def test_international_trade_redirect(client):
    url = reverse('international-trade', kwargs={'path': 'foo/bar'})

    response = client.get(url)

    assert response.status_code == 302
    print('response url: ' + response.url)
    print('expected url: ' + urls.international.TRADE_HOME + 'incoming/foo/bar')
    assert response.url == urls.international.TRADE_HOME + 'incoming/foo/bar'


def test_international_investment_support_directory_redirect_home(client):
    url = reverse('international-investment-support-directory-home')
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == urls.international.EXPAND_ISD_HOME


def test_international_investment_support_directory_redirect(client):
    url = reverse('international-investment-support-directory', kwargs={'path': 'foo/bar'})

    response = client.get(url)

    assert response.status_code == 302
    assert response.url == urls.international.EXPAND_ISD_HOME + 'foo/bar'


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@patch('directory_cms_client.client.cms_api_client.list_industry_tags', mock.MagicMock())
def test_new_landing_page_querystring_old_cms_page(mock_page, client):
    mock_page.return_value = create_response({
        'page_type': 'HomePage',
        'tree_based_breadcrumbs': [
            {'title': 'great.gov.uk', 'url': '/'}
        ],
    })

    content_list_industry_tags = [{}]
    create_response(content_list_industry_tags)
    url = '/'
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['core/landing_page.html']


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@patch('directory_cms_client.client.cms_api_client.list_industry_tags', mock.MagicMock())
def test_new_landing_page_querystring_new_cms_page(mock_page, client):
    mock_page.return_value = create_response({
        'page_type': 'HomePage',
        'tree_based_breadcrumbs': [
            {'title': 'great.gov.uk', 'url': '/'}
        ],
        'how_dit_helps_title': '',
        'hero_text': '',
        'questions_section_title': '',
        'what_is_new_title': '',
    })

    content_list_industry_tags = [{}]
    create_response(content_list_industry_tags)
    url = '/'
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['core/landing_page.html']


@pytest.mark.parametrize(
    'page_type,expected_template',
    [
        ('ArticleListingPage', 'content/article_list.html'),
        ('TopicLandingPage', 'content/topic_list.html'),
        ('ArticlePage', 'content/article_detail.html'),
    ]
)
@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_cms_path_lookup(mock_page, page_type, expected_template, client):
    mock_page.return_value = create_response({
        'page_type': page_type,
        'title': 'Page title',
        'tree_based_breadcrumbs': [
            {'title': 'great.gov.uk', 'url': '/'},
            {'title': 'Article list', 'url': '/article-list'},
        ],
        'slug': 'test',
    })

    response = client.get('/test/')

    assert response.status_code == 200
    assert response.template_name == [expected_template]


@patch('directory_cms_client.client.cms_api_client.lookup_by_path')
def test_cms_path_url(mock_page, client):
    mock_page.return_value = create_response({
        'page_type': 'ArticlePage',
        'title': 'Page title',
        'tree_based_breadcrumbs': [
            {'title': 'great.gov.uk', 'url': '/'},
            {'title': 'Article', 'url': '/test-article/'}
        ],
        'meta': {'slug': 'test-article'},
    })

    response = client.get('/test-article/')

    assert response.status_code == 200
    assert response.template_name == ['content/article_detail.html']
