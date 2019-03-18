import json
import http
from unittest.mock import call, patch, PropertyMock, Mock

import requests

from django.core.urlresolvers import reverse
from django.conf import settings
from django.views.generic import TemplateView

from bs4 import BeautifulSoup
import pytest
import requests_mock
from rest_framework import status

from core import helpers, views
from core.tests.helpers import create_response
from casestudy import casestudies

from directory_constants.constants import cms


def test_interstitial_page_exopps(client):
    url = reverse('export-opportunities')
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == settings.SERVICES_EXOPPS_ACTUAL


@patch(
    'core.helpers.GeoLocationRedirector.should_redirect',
    PropertyMock(return_value=True)
)
@patch(
    'core.helpers.GeoLocationRedirector.country_language',
    PropertyMock(return_value='fr')
)
def test_landing_page_redirect(client):
    url = reverse('landing-page')

    response = client.get(url)

    assert response.status_code == 302
    assert response.url == (
        reverse('landing-page-international') + '?lang=' + 'fr'
    )
    assert response.cookies[helpers.GeoLocationRedirector.COOKIE_NAME].value


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_landing_page(mock_get_page, client, settings):
    settings.FEATURE_FLAGS['NEWS_SECTION_ON'] = False
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = False

    page = {
        'news_title': 'News',
        'news_description': '<p>Lorem ipsum</p>',
        'articles': [
            {'article_title': 'News article 1'},
            {'article_title': 'News article 2'},
        ],
        'guidance': [
            {'landing_page_title': 'Guidance 1'},
            {'landing_page_title': 'Guidance 2'},
        ],
    }

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=page
    )

    url = reverse('landing-page')

    response = client.get(url)

    assert response.status_code == 200
    assert '/static/js/home' in str(response.content)
    assert response.template_name == [
        views.LandingPageView.template_name]
    assert response.context_data['casestudies'] == [
        casestudies.MARKETPLACE,
        casestudies.HELLO_BABY,
        casestudies.YORK,
    ]


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_landing_page_video_url(mock_get_page, client, settings):
    settings.FEATURE_FLAGS['NEWS_SECTION_ON'] = False
    settings.FEATURE_FLAGS['LANDING_PAGE_EU_EXIT_BANNER_ON'] = False

    settings.LANDING_PAGE_VIDEO_URL = 'https://example.com/videp.mp4'

    url = reverse('landing-page')
    response = client.get(url)
    assert response.context_data['LANDING_PAGE_VIDEO_URL'] == (
        'https://example.com/videp.mp4'
    )
    assert b'https://example.com/videp.mp4' in response.content


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_landing_page_news_and_export_journey_off(
    mock_get_page, client, settings
):
    settings.FEATURE_FLAGS['NEWS_SECTION_ON'] = False
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = False

    page = {
        'news_title': 'News',
        'news_description': '<p>Lorem ipsum</p>',
        'articles': [
            {'article_title': 'News article 1'},
            {'article_title': 'News article 2'},
        ],
        'guidance': [
            {'landing_page_title': 'Guidance 1'},
            {'landing_page_title': 'Guidance 2'},
        ],
    }

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=page
    )

    url = reverse('landing-page')

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [views.LandingPageView.template_name]


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_landing_page_template_news_feature_flag_on(
    mock_get_page, client, settings
):
    settings.FEATURE_FLAGS['NEWS_SECTION_ON'] = True
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = False

    page = {
        'news_title': 'News',
        'news_description': '<p>Lorem ipsum</p>',
        'articles': [
            {'article_title': 'News article 1'},
            {'article_title': 'News article 2'},
        ],
        'guidance': [
            {'landing_page_title': 'Guidance 1'},
            {'landing_page_title': 'Guidance 2'},
        ],
    }

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=page
    )

    url = reverse('landing-page')

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [views.LandingPageView.template_name]


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_landing_page_template_news_feature_flag_off(
    mock_get_page, client, settings
):
    settings.FEATURE_FLAGS['NEWS_SECTION_ON'] = False

    page = {
        'news_title': 'News',
        'news_description': '<p>Lorem ipsum</p>',
        'articles': [
            {'article_title': 'News article 1'},
            {'article_title': 'News article 2'},
        ],
        'guidance': [
            {'landing_page_title': 'Guidance 1'},
            {'landing_page_title': 'Guidance 2'},
        ],
    }

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=page
    )

    url = reverse('landing-page')
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [views.LandingPageView.template_name]


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
            'about',
            'core/about.html'
        ),
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
        (
            'terms-and-conditions-international',
            'core/info_page_international.html'
        ),
    )
)
@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_terms_conditions_cms(
    mock_get_t_and_c_page, view, expected_template, client
):
    url = reverse(view)
    page = {
        'title': 'the page',
        'industries': [{'title': 'good 1'}],
        'meta': {'languages': ['en-gb']},
    }
    mock_get_t_and_c_page.return_value = create_response(
        status_code=200,
        json_body=page
    )
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [expected_template]


@pytest.mark.parametrize(
    'view,expected_template',
    (
        (
            'privacy-and-cookies',
            'core/info_page.html'
        ),
        (
            'privacy-and-cookies-international',
            'core/info_page_international.html'
        ),
    )
)
@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_privacy_cookies_cms(
    mock_get_p_and_c_page, view, expected_template, client
):
    url = reverse(view)
    page = {
        'title': 'the page',
        'industries': [{'title': 'good 1'}],
        'meta': {'languages': ['en-gb']},
    }
    mock_get_p_and_c_page.return_value = create_response(
        status_code=200,
        json_body=page
    )
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [expected_template]


@pytest.mark.parametrize(
    'activated_language,component_languages,direction',
    (
        (
            'ar', [['ar', 'العربيّة'], ['en-gb', 'English']], 'rtl'
        ),
        (
            'en-gb', [['ar', 'العربيّة'], ['en-gb', 'English']], 'ltr'
        ),
        (
            'zh-hans', [['ar', 'العربيّة'], ['en-gb', 'English']], 'ltr'
        ),
    )
)
@patch('core.views.InternationalLandingPageView.cms_component',
       new_callable=PropertyMock)
@patch('core.views.InternationalLandingPageView.page',
       new_callable=PropertyMock)
def test_international_landing_page_news_section_on(
    mock_get_page, mock_get_component, activated_language,
    component_languages, direction, client, settings
):
    settings.FEATURE_FLAGS['NEWS_SECTION_ON'] = True
    mock_get_page.return_value = {
        'title': 'the page',
        'articles_count': 1,
        'meta': {'languages': [['en-gb', 'English']]},
    }
    mock_get_component.return_value = {
        'banner_label': 'EU exit updates',
        'banner_content': '<p>Lorem ipsum.</p>',
        'meta': {'languages': component_languages},
    }

    url = reverse('landing-page-international')
    response = client.get(url, {'lang': activated_language})

    assert response.template_name == ['core/landing_page_international.html']
    assert 'EU exit updates' in str(response.content)
    assert '<p class="body-text">Lorem ipsum.</p>' in str(response.content)

    soup = BeautifulSoup(response.content, 'html.parser')
    component = soup.select('.banner-container')[0]
    assert component.attrs['dir'] == direction


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@patch('core.views.InternationalLandingPageView.page',
       new_callable=PropertyMock)
def test_international_landing_page_news_section_off(
    mock_get_page, mock_get_component, client, settings
):
    settings.FEATURE_FLAGS['NEWS_SECTION_ON'] = False
    mock_get_page.return_value = {
        'title': 'the page',
        'articles_count': 1,
        'meta': {'languages': [['en-gb', 'English']]},
    }
    mock_get_component.return_value = create_response(
        status_code=200,
        json_body={
            'banner_label': 'EU exit updates',
            'banner_content': '<p>Lorem ipsum.</p>',
            'meta': {'languages': [['en-gb', 'English']]},
        }
    )

    url = reverse('landing-page-international')
    response = client.get(url)

    assert 'EU exit updates' not in str(response.content)


@patch('core.views.InternationalLandingPageView.cms_component',
       new_callable=PropertyMock)
@patch('core.views.InternationalLandingPageView.page',
       new_callable=PropertyMock)
def test_international_landing_page_no_articles(
    mock_get_page, mock_get_component, client, settings
):
    settings.FEATURE_FLAGS['NEWS_SECTION_ON'] = False
    mock_get_page.return_value = {
        'title': 'the page',
        'articles_count': 0,
        'meta': {'languages': [['en-gb', 'English']]},
    }
    mock_get_component.return_value = {
        'banner_label': 'EU exit updates',
        'banner_content': '<p>Lorem ipsum.</p>',
        'meta': {'languages': [['en-gb', 'English']]},
    }

    url = reverse('landing-page-international')
    response = client.get(url)

    assert 'EU exit updates' not in str(response.content)


@patch('core.views.InternationalLandingPageView.cms_component',
       new_callable=PropertyMock)
@patch('core.views.InternationalLandingPageView.page',
       new_callable=PropertyMock)
@pytest.mark.parametrize("lang", ['ar', 'es', 'zh-hans', 'pt', 'de', 'ja'])
def test_international_landing_view_translations(
    mock_get_page, mock_get_component, lang, client
):
    response = client.get(
        reverse('landing-page-international'),
        {'lang': lang}
    )
    mock_get_page.return_value = {
        'title': 'the page',
        'articles_count': 0,
        'meta': {'languages': [['en-gb', 'English']]},
    }
    mock_get_component.return_value = {
        'banner_label': 'EU exit updates',
        'banner_content': '<p>Lorem ipsum.</p>',
        'meta': {'languages': [['en-gb', 'English']]},
    }

    assert response.status_code == http.client.OK
    assert response.cookies['django_language'].value == lang


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
    request.sso_user = None
    view = MyView.as_view()
    response = view(request)

    response.render()
    assert response.get('Etag') == expected


@pytest.mark.parametrize('view_class', views.SetEtagMixin.__subclasses__())
def test_cached_views_not_dynamic(rf, settings, view_class):
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


def test_about_view(client):
    response = client.get(reverse('about'))

    assert response.status_code == 200
    assert response.template_name == [views.AboutView.template_name]


def test_search_view(client):
    """ We mock the call to ActivityStream """
    with patch('core.helpers.search_with_activitystream') as search:
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

        response = client.get("%s?q=services" % reverse('search'))
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

        response = client.get("%s?q=services" % reverse('search'))
        context = response.context_data

        assert response.status_code == 200
        assert context['results'] == []

        """ What if ActivitySteam sends an error? """
        search.return_value = Mock(status_code=500,
                                   content="[service overloaded]")

        response = client.get("%s?q=Document" % reverse('search'))
        context = response.context_data

        assert response.status_code == 200
        # This can be handled on the front end as we wish
        assert context['error_message'] == "[service overloaded]"
        assert context['error_status_code'] == 500

        """ What if ActivitySteam is down? """
        search.side_effect = requests.exceptions.ConnectionError

        response = client.get("%s?q=Document" % reverse('search'))
        context = response.context_data

        assert response.status_code == 200
        # This can be handled on the front end as we wish
        assert context['error_message'] == "Activity Stream connection failed"
        assert context['error_status_code'] == 500


cms_urls_slugs = (
    (
        reverse('privacy-and-cookies'),
        cms.GREAT_PRIVACY_AND_COOKIES_SLUG,
    ),
    (
        reverse('terms-and-conditions'),
        cms.GREAT_TERMS_AND_CONDITIONS_SLUG,
    ),
    (
        reverse('privacy-and-cookies-international'),
        cms.GREAT_PRIVACY_AND_COOKIES_SLUG,
    ),
    (
        reverse('terms-and-conditions-international'),
        cms.GREAT_TERMS_AND_CONDITIONS_SLUG,
    ),
)


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@pytest.mark.parametrize('url,slug', cms_urls_slugs)
def test_cms_pages_cms_client_params(mock_get, client, url, slug):
    mock_get.return_value = create_response(status_code=200)

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
    reverse('privacy-and-cookies-international'),
    reverse('terms-and-conditions-international'),
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
    }
    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=page
    )
    response = client.get(url)

    assert page['title'] in str(response.content)
    assert page['heading'] in str(response.content)
    assert page['description'] in str(response.content)

    assert response.status_code == 200
    assert response.template_name == ['core/performance_dashboard.html']


def test_performance_dashboard_feature_flag_off(client, settings):
    settings.FEATURE_FLAGS['PERFORMANCE_DASHBOARD_ON'] = False

    response = client.get('performance-dashboard')

    assert response.status_code == 404


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_privacy_cookies_subpage(mock_get_page, client, settings):
    url = reverse('privacy-and-cookies-subpage', kwargs={
        'slug': 'fair-processing-notice-zendesk'
    })
    page = {
        'title': 'Fair Processing Notice Zendesk',
        'body': 'Lorem ipsum dolor sit amet.',
    }
    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=page
    )
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['core/privacy_subpage.html']

    assert page['title'] in str(response.content)
    assert page['body'] in str(response.content)


def test_international_contact_page_context(client, settings):
    url = reverse('contact-page-international')
    response = client.get(url)

    assert response.context_data['invest_contact_us_url'] == (
        'http://invest.trade.great:8012/contact/'
    )


campaign_page_all_fields = {
    'campaign_heading': 'Campaign heading',
    'campaign_hero_image': {'url': 'campaign_hero_image.jpg'},
    'cta_box_button_text': 'CTA box button text',
    'cta_box_button_url': '/cta_box_button_url',
    'cta_box_message': 'CTA box message',
    'related_content_heading': 'Related content heading',
    'related_content_intro': '<p>Related content intro.</p>',
    'section_one_contact_button_text': 'Section one contact button text',
    'section_one_contact_button_url': '/section_one_contact_button_url',
    'section_one_heading': 'Section one heading',
    'section_one_image': {'url': 'section_one_image.jpg'},
    'section_one_intro': '<p>Section one intro.</p>',
    'section_two_contact_button_text': 'Section one contact button text',
    'section_two_contact_button_url': '/section_two_contact_button_url',
    'section_two_heading': 'Section two heading',
    'section_two_image': {'url': 'section_two_image.jpg'},
    'section_two_intro': '<p>Section two intro</p>',
    'selling_point_one_content': '<p>Selling point one content</p>',
    'selling_point_one_heading': 'Selling point one heading',
    'selling_point_one_icon': {'url': 'selling_point_one_icon.jpg'},
    'selling_point_two_content': '<p>Selling point two content</p>',
    'selling_point_two_heading': 'Selling point two heading',
    'selling_point_two_icon': {'url': 'selling_point_two_icon.jpg'},
    'selling_point_three_content': '<p>Selling point three content</p>',
    'selling_point_three_heading': 'Selling point three heading',
    'selling_point_three_icon': {'url': 'selling_point_three_icon.jpg'},
    'related_pages': [
        {
            'article_image': {'url': 'article_image.jpg'},
            'article_image_thumbnail': {'url': 'article1_image_thumbnail.jpg'},
            'article_teaser': 'Related article description 1',
            'article_title': 'Related article 1',
            'full_path': '/advice/finance/article-1/',
            'meta': {
                'languages': [['en-gb', 'English']],
                'slug': 'article-1'},
            'page_type': 'ArticlePage',
            'title': 'Related article 1'
        },
        {
            'article_image': {'url': 'article_image.jpg'},
            'article_image_thumbnail': {'url': 'article2_image_thumbnail.jpg'},
            'article_teaser': 'Related article description 2',
            'article_title': 'Related article 2',
            'full_path': '/advice/finance/article-2/',
            'meta': {
                'languages': [['en-gb', 'English']],
                'slug': 'article-2'},
            'page_type': 'ArticlePage',
            'title': 'Related article 2'
        },
        {
            'article_image': {'url': 'article_image.jpg'},
            'article_image_thumbnail': {'url': 'article3_image_thumbnail.jpg'},
            'article_teaser': 'Related article description 3',
            'article_title': 'Related article 3',
            'full_path': '/advice/finance/article-3/',
            'meta': {
                'languages': [['en-gb', 'English']],
                'slug': 'article-3'},
            'page_type': 'ArticlePage',
            'title': 'Related article 3'
        },
    ],
}


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_marketing_campaign_campaign_page_all_fields(
    mock_get_page, client, settings
):
    settings.FEATURE_FLAGS['CAMPAIGN_PAGES_ON'] = True

    url = reverse('campaign-page', kwargs={'slug': 'test-page'})

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=campaign_page_all_fields
    )
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['core/campaign.html']

    soup = BeautifulSoup(response.content, 'html.parser')

    assert ('<p class="body-text">Selling point two content</p>'
            ) in str(response.content)

    assert ('<p class="body-text">Selling point three content</p>'
            ) in str(response.content)

    hero_section = soup.find(id='campaign-hero')

    exp_style = "background-image: url('{}')".format(
        campaign_page_all_fields['campaign_hero_image']['url'])

    assert hero_section.attrs['style'] == exp_style

    assert soup.find(
        id='selling-points-icon-two').attrs['src'] == campaign_page_all_fields[
        'selling_point_two_icon']['url']

    assert soup.find(
        id='selling-points-icon-three'
    ).attrs['src'] == campaign_page_all_fields[
        'selling_point_three_icon']['url']

    assert soup.find(
        id='section-one-contact-button'
    ).attrs['href'] == campaign_page_all_fields[
        'section_one_contact_button_url']
    assert soup.find(
        id='section-one-contact-button').text == campaign_page_all_fields[
        'section_one_contact_button_text']

    assert soup.find(
        id='section-two-contact-button'
    ).attrs['href'] == campaign_page_all_fields[
        'section_two_contact_button_url']
    assert soup.find(
        id='section-two-contact-button').text == campaign_page_all_fields[
        'section_two_contact_button_text']

    related_page_one = soup.find(id='related-page-article-1')
    assert related_page_one.find('a').text == 'Related article 1'
    assert related_page_one.find('p').text == 'Related article description 1'
    assert related_page_one.find('a').attrs['href'] == (
        '/advice/finance/article-1/')
    assert related_page_one.find('img').attrs['src'] == (
        'article1_image_thumbnail.jpg')

    related_page_two = soup.find(id='related-page-article-2')
    assert related_page_two.find('a').text == 'Related article 2'
    assert related_page_two.find('p').text == 'Related article description 2'
    assert related_page_two.find('a').attrs['href'] == (
        '/advice/finance/article-2/')
    assert related_page_two.find('img').attrs['src'] == (
        'article2_image_thumbnail.jpg')

    related_page_three = soup.find(id='related-page-article-3')
    assert related_page_three.find('a').text == 'Related article 3'
    assert related_page_three.find('p').text == 'Related article description 3'
    assert related_page_three.find('a').attrs['href'] == (
        '/advice/finance/article-3/')
    assert related_page_three.find('img').attrs['src'] == (
        'article3_image_thumbnail.jpg')


campaign_page_required_fields = {
    'campaign_heading': 'Campaign heading',
    'campaign_hero_image': None,
    'cta_box_button_text': 'CTA box button text',
    'cta_box_button_url': '/cta_box_button_url',
    'cta_box_message': 'CTA box message',
    'related_content_heading': 'Related content heading',
    'related_content_intro': '<p>Related content intro.</p>',
    'related_pages': [],
    'section_one_contact_button_text': None,
    'section_one_contact_button_url': None,
    'section_one_heading': 'Section one heading',
    'section_one_image': None,
    'section_one_intro': '<p>Section one intro.</p>',
    'section_two_contact_button_text': None,
    'section_two_contact_button_url': None,
    'section_two_heading': 'Section two heading',
    'section_two_image': None,
    'section_two_intro': '<p>Section two intro</p>',
    'selling_point_one_content': '<p>Selling point one content</p>',
    'selling_point_one_heading': 'Selling point one heading',
    'selling_point_one_icon': None,
    'selling_point_two_content': '<p>Selling point two content</p>',
    'selling_point_two_heading': 'Selling point two heading',
    'selling_point_two_icon': None,
    'selling_point_three_content': '<p>Selling point three content</p>',
    'selling_point_three_heading': 'Selling point three heading',
    'selling_point_three_icon': None,
}


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_marketing_campaign_page_required_fields(
    mock_get_page, client, settings
):
    settings.FEATURE_FLAGS['CAMPAIGN_PAGES_ON'] = True

    url = reverse('campaign-page', kwargs={'slug': 'test-page'})

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=campaign_page_required_fields
    )
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['core/campaign.html']

    soup = BeautifulSoup(response.content, 'html.parser')

    assert ('<p class="body-text">Selling point two content</p>'
            ) in str(response.content)

    assert ('<p class="body-text">Selling point three content</p>'
            ) in str(response.content)

    hero_section = soup.find(id='campaign-hero')
    assert not hero_section.attrs.get('style')

    assert not soup.find(id='selling-points-icon-two')
    assert not soup.find(id='selling-points-icon-three')

    assert not soup.find(id='section-one-contact-button')
    assert not soup.find(id='section-one-contact-button')

    assert not soup.find(id='section-two-contact-button')
    assert not soup.find(id='section-two-contact-button')

    assert soup.select(
        '#campaign-contact-box .box-heading'
        )[0].text == campaign_page_required_fields['cta_box_message']

    assert soup.find(
        id='campaign-hero-heading'
        ).text == campaign_page_required_fields['campaign_heading']

    assert soup.find(
        id='section-one-heading'
        ).text == campaign_page_required_fields['section_one_heading']

    assert soup.find(
        id='section-two-heading'
        ).text == campaign_page_required_fields['section_two_heading']

    assert soup.find(
        id='related-content-heading'
        ).text == campaign_page_required_fields['related_content_heading']

    assert soup.select(
        "li[aria-current='page']"
        )[0].text == campaign_page_required_fields['campaign_heading']


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_marketing_campaign_page_feature_flag_off(
    mock_get_page, client, settings
):
    settings.FEATURE_FLAGS['CAMPAIGN_PAGES_ON'] = False

    url = reverse('campaign-page', kwargs={'slug': 'test-page'})

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=campaign_page_required_fields
    )
    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.parametrize('view_name', ['triage-start', 'custom-page'])
def test_triage_views(view_name, client):
    url = reverse(view_name)
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.template_name == ['core/service_no_longer_available.html']


def test_triage_wizard_view(client):
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

    mock_search.return_value = create_response(400)
    url = reverse('api-internal-companies-house-search')

    with pytest.raises(requests.HTTPError):
        client.get(url, data={'term': 'thing'})


@patch('core.helpers.CompaniesHouseClient.search')
def test_companies_house_search_api_success(mock_search, client, settings):
    settings.FEATURE_FLAGS['INTERNAL_CH_ON'] = False

    mock_search.return_value = create_response(
        200, {'items': [{'name': 'Smashing corp'}]}
    )
    url = reverse('api-internal-companies-house-search')

    response = client.get(url, data={'term': 'thing'})

    assert response.status_code == 200
    assert response.content == b'[{"name": "Smashing corp"}]'


@patch('core.helpers.CompanyCHClient')
def test_companies_house_search_internal(mocked_ch_client, client, settings):
    settings.FEATURE_FLAGS['INTERNAL_CH_ON'] = True

    mocked_ch_client().search_companies.return_value = create_response(
        200, {'items': [{'name': 'Smashing corp'}]}
    )
    url = reverse('api-internal-companies-house-search')

    response = client.get(url, data={'term': 'thing'})

    assert response.status_code == 200
    assert response.content == b'[{"name": "Smashing corp"}]'
