from unittest import mock

import pytest
from unittest.mock import patch
from bs4 import BeautifulSoup
from django.template.loader import render_to_string
from core.tests.helpers import create_response
from django.urls import reverse
from directory_components.context_processors import urls_processor
from django.core.paginator import Paginator


def test_market_landing_pagination_page_next(rf, context):

    page_size = 18
    child_page = {'title': 'Title', 'sub_heading': 'Markets subheading'}
    page = {
        'title': 'test',
        'page_type': 'TopicLandingPage',
        'tree_based_breadcrumbs': [
            {'url': '/markets/', 'title': 'Markets'},
            {'url': '/markets/japan/', 'title': 'Japan'},
        ],
        'child_pages': [
            child_page,
            child_page,
            child_page,
            child_page,
            child_page,
            child_page,
            child_page,
            child_page,
            child_page,
            child_page,
            child_page,
            child_page,
            child_page,
            child_page,
            child_page,
            child_page,
            child_page,
            child_page,
            child_page,
            child_page
        ]
    }

    paginator = Paginator(page['child_pages'], page_size)
    pagination_page = paginator.page(1)
    context['request'] = rf.get('/')
    context['pagination_page'] = pagination_page

    html = render_to_string('content/markets_landing_page.html', context)

    assert len(pagination_page) == 18
    assert 'pagination-next' in html


def test_market_landing_pagination_page_next_not_in_html(rf, context):

    page_size = 18
    child_page = {'title': 'Title', 'sub_heading': 'Markets subheading'}
    page = {
        'title': 'test',
        'page_type': 'TopicLandingPage',
        'tree_based_breadcrumbs': [
            {'url': '/markets/', 'title': 'Markets'},
            {'url': '/markets/japan/', 'title': 'Japan'},
        ],
        'child_pages': [
            child_page,
            child_page,
            child_page,
            child_page,
            child_page,
            child_page,
            child_page,
            child_page,
            child_page,
            child_page
        ]
    }

    paginator = Paginator(page['child_pages'], page_size)
    pagination_page = paginator.page(1)
    context['request'] = rf.get('/')
    context['pagination_page'] = pagination_page

    html = render_to_string('content/markets_landing_page.html', context)

    assert 'pagination-next' not in html


def test_article_detail_page_no_related_content(rf, context):
    page = {
        "title": "Test article admin title",
        "article_title": "Test article",
        "article_teaser": "Test teaser",
        "article_image": {"url": "foobar.png"},
        "article_body_text": "<p>Lorem ipsum</p>",
        "related_pages": [],
        "full_path": "/advice/manage-legal-and-ethical-compliance/foo/",
        "last_published_at": "2018-10-09T16:25:13.142357Z",
        "meta": {
            "slug": "foo",
        },
        "page_type": "ArticlePage",
    }
    context['request'] = rf.get('/')
    context['page'] = page

    html = render_to_string('content/article_detail.html', context)
    assert 'Related content' not in html


def test_article_advice_page(context):
    page = {
        'title': 'Markets',
        'hero_image': {'url': 'markets.jpg'},
        'child_pages': [
            {
                'title': 'Africa market information',
                'full_path': '/markets/africa/',
                'hero_image': {'url': 'africa.png'},
                'hero_image_thumbnail': {'url': 'africa.jpg'},
                'articles_count': 0,
            },
            {
                'title': 'Asia market information',
                'full_path': '/markets/asia/',
                'hero_image': {'url': 'asia.png'},
                'hero_image_thumbnail': {'url': 'asia.jpg'},
                'articles_count': 3,
            }
        ],
        "page_type": "TopicLandingPage",
    }

    context['page'] = page

    html = render_to_string('content/topic_list.html', context)

    assert page['title'] in html

    assert 'Asia market information' in html
    assert 'Africa market information' in html
    assert 'markets.jpg' in html
    assert 'asia.jpg' in html
    assert 'africa.jpg' in html


def test_article_detail_page_related_content(rf, context):
    context['request'] = rf.get('/')
    page = {
        "title": "Test article admin title",
        "article_title": "Test article",
        "article_teaser": "Test teaser",
        "article_image": {"url": "foobar.png"},
        "article_body_text": "<p>Lorem ipsum</p>",
        "cta_title": 'CTA title',
        "cta_teaser": 'CTA teaser text',
        "cta_link_label": "CTA link label",
        "cta_link": "http://www.great.gov.uk",
        "last_published_at": "2018-10-09T16:25:13.142357Z",
        "meta": {
            "slug": "bar",
        },
        "related_pages": [
            {
                "article_title": "Related article 1",
                "full_path": "/markets/test/test-one",
                "meta": {
                    "slug": "test-one",
                }
            },
            {
                "article_title": "Related article 2",
                "full_path": "/markets/test/test-two",
                "meta": {
                    "slug": "test-two",
                }
            },
        ],
        "page_type": "ArticlePage",
    }
    context['page'] = page
    html = render_to_string('content/article_detail.html', context)
    soup = BeautifulSoup(html, 'html.parser')

    assert 'Related content' in html
    assert soup.find(id='related-content').select('li a')[0].attrs['href'] == '/markets/test/test-one'
    assert soup.find(id='related-content').select('li a')[0].text == 'Related article 1'
    assert soup.find(id='related-content').select('li a')[1].attrs['href'] == '/markets/test/test-two'
    assert soup.find(id='related-content').select('li a')[1].text == 'Related article 2'


def test_article_detail_page_related_content_footer(rf, context):
    context['request'] = rf.get('/')
    page = {
        "title": "Test article admin title",
        "article_title": "Test article",
        "article_teaser": "Test teaser",
        "article_image": {"url": "foobar.png"},
        "article_body_text": "<p>Lorem ipsum</p>",
        "cta_title": 'CTA title',
        "cta_teaser": 'CTA teaser text',
        "cta_link_label": "CTA link label",
        "cta_link": "http://www.great.gov.uk",
        "last_published_at": "2018-10-09T16:25:13.142357Z",
        "meta": {
            "slug": "bar",
        },
        "page_type": "ArticlePage",
    }
    context['page'] = page

    html = render_to_string('content/article_detail.html', context)

    soup = BeautifulSoup(html, 'html.parser')
    assert soup.find(
        id='article_related_content_footer'
    ).select('h2')[0].text == 'CTA title'

    assert soup.find(
        id='article_related_content_footer'
    ).select('p')[0].text == 'CTA teaser text'

    assert soup.find(
        id='article_related_content_footer'
    ).select('a.button')[0].attrs['href'] == 'http://www.great.gov.uk'


def test_article_detail_page_related_content_footer_not_rendered(rf, context):
    context['request'] = rf.get('/')
    page = {
        "title": "Test article admin title",
        "article_title": "Test article",
        "article_teaser": "Test teaser",
        "article_image": {"url": "foobar.png"},
        "article_body_text": "<p>Lorem ipsum</p>",
        "cta_title": '',
        "cta_teaser": '',
        "cta_link_label": "",
        "cta_link": "",
        "last_published_at": "2018-10-09T16:25:13.142357Z",
        "meta": {
            "slug": "bar",
        },
        "page_type": "ArticlePage",
    }

    context['page'] = page

    html = render_to_string('content/article_detail.html', context)

    assert '<section id="article_related_content_footer"' not in html


def test_article_detail_page_media_rendered(rf, context):
    context['request'] = rf.get('/')
    page = {
        "article_video": {
            "url": "test.mp4",
            "file_extension": "mp4"
        }
    }

    context['page'] = page

    html = render_to_string('content/article_detail.html', context)

    soup = BeautifulSoup(html, 'html.parser')
    src = soup.find(id='article-video').select('source')[0]

    assert '<div class="video-container">' in html
    assert src.attrs['src'] == 'test.mp4'
    assert src.attrs['type'] == 'video/mp4'


def test_article_detail_page_media_not_rendered(rf, context):
    context['request'] = rf.get('/')
    page = {
        "title": "Test article admin title",
        "article_title": "Test article",
        "article_teaser": "Test teaser",
        "article_image": {"url": "foobar.png"},
        "article_body_text": "<p>Lorem ipsum</p>",
        "cta_title": 'CTA title',
        "cta_teaser": 'CTA teaser text',
        "cta_link_label": "CTA link label",
        "cta_link": "http://www.great.gov.uk",
        "last_published_at": "2018-10-09T16:25:13.142357Z",
    }

    context['page'] = page

    html = render_to_string('content/article_detail.html', context)

    assert '<div class="video-container">' not in html


def test_marketing_article_detail_page_related_content(rf, context):
    page = {
        "title": "Test article admin title",
        "article_title": "Test article",
        "article_teaser": "Test teaser",
        "article_image": {"url": "foobar.png"},
        "article_body_text": "<p>Lorem ipsum</p>",
        "cta_title": 'CTA title',
        "cta_teaser": 'CTA teaser text',
        "cta_link_label": "CTA link label",
        "cta_link": "http://www.great.gov.uk",
        "last_published_at": "2018-10-09T16:25:13.142357Z",
        "meta": {
            "slug": "bar",
        },
        "page_type": "MarketingArticlePage",
    }
    context['request'] = rf.get('/')
    context['page'] = page
    html = render_to_string('content/marketing_article_detail.html', context)

    soup = BeautifulSoup(html, 'html.parser')
    assert soup.find(id='contact-us-section').select('h2')[0].text == 'CTA title'
    assert soup.find(id='contact-us-section').select('p')[0].text == 'CTA teaser text'
    assert soup.find(id='contact-us-section').select('a.button')[0].attrs['href'] == 'http://www.great.gov.uk'


def test_marketing_article_detail_page_related_content_not_rendered(rf, context):
    page = {
        "title": "Test article admin title",
        "article_title": "Test article",
        "article_teaser": "Test teaser",
        "article_image": {"url": "foobar.png"},
        "article_body_text": "<p>Lorem ipsum</p>",
        "cta_title": '',
        "cta_teaser": '',
        "cta_link_label": "",
        "cta_link": "",
        "last_published_at": "2018-10-09T16:25:13.142357Z",
        "meta": {
            "slug": "bar",
        },
        "page_type": "MarketingArticlePage",
    }

    context['request'] = rf.get('/')
    context['page'] = page

    html = render_to_string('content/marketing_article_detail.html', context)

    assert '<section id="contact-us-section"' not in html


def test_marketing_article_detail_content_button_not_rendered_without_link(rf, context):
    page = {
        "title": "Test article admin title",
        "article_title": "Test article",
        "article_teaser": "Test teaser",
        "article_image": {"url": "foobar.png"},
        "article_body_text": "<p>Lorem ipsum</p>",
        "cta_title": 'CTA title',
        "cta_teaser": 'CTA teaser text',
        "cta_link_label": "CTA link label",
        "cta_link": "",
        "last_published_at": "2018-10-09T16:25:13.142357Z",
        "meta": {
            "slug": "bar",
        },
        "page_type": "MarketingArticlePage",
    }

    context['request'] = rf.get('/')
    context['page'] = page

    html = render_to_string('content/marketing_article_detail.html', context)

    assert 'class="button button-arrow-small"' not in html


test_news_list_page = {
    'title': 'News',
    'articles_count': 2,
    'articles': [
        {
            'article_title': 'Lorem ipsum',
            'full_path': '/eu-exit-news/lorem-ipsum/',
            'last_published_at': '2018-10-01T15:15:53.927833Z',
            'meta': {'slug': 'test-slug-one'},
        },
        {
            'article_title': 'Dolor sit amet',
            'full_path': '/eu-exit-news/dolor-sit-amet/',
            'last_published_at': '2018-10-01T15:16:30.583279Z',
            'meta': {'slug': 'test-slug-two'},
        }
    ],
    "page_type": "ArticleListingPage",
}


def test_news_list_page_feature_flag_on(context):
    context['features'] = {'NEWS_SECTION_ON': True}
    context['page'] = test_news_list_page

    html = render_to_string('content/domestic_news_list.html', context)

    assert test_news_list_page['title'] in html
    assert 'Lorem ipsum' in html
    assert 'Dolor sit amet' in html


test_articles = [
    {
        'seo_title': 'SEO title article 1',
        'search_description': 'Search description article 1',
        'article_title': 'Article 1 title',
        'article_teaser': 'Article 1 teaser.',
        'article_image': {'url': 'article_image1.png'},
        'article_body_text': '<p>Lorem ipsum 1</p>',
        'last_published_at': '2018-10-01T15:16:30.583279Z',
        'full_path': '/topic/list/article-one/',
        'tags': [
            {'name': 'New to exporting', 'slug': 'new-to-exporting'},
            {'name': 'Export tips', 'slug': 'export-tips'}
        ],
        'meta': {'slug': 'article-one'}
    },
    {
        'seo_title': 'SEO title article 2',
        'search_description': 'Search description article 2',
        'article_title': 'Article 2 title',
        'article_teaser': 'Article 2 teaser.',
        'article_image': {'url': 'article_image2.png'},
        'article_body_text': '<p>Lorem ipsum 2</p>',
        'last_published_at': '2018-10-02T15:16:30.583279Z',
        'full_path': '/topic/list/article-two/',
        'tags': [
            {'name': 'New to exporting', 'slug': 'new-to-exporting'},
        ],
        'meta': {'slug': 'article-two'}
    },
]

test_list_page = {
    'seo_title': 'SEO title article list',
    'search_description': 'Article list search description',
    'title': 'Article list landing page title',
    'hero_image': {'url': 'article_list.png'},
    'hero_teaser': 'Article list hero teaser',
    'list_teaser': '<p>Article list teaser</p>',
    'articles': test_articles,
    'page_type': 'ArticleListingPage',
}


def test_article_list_page(context):
    context['page'] = test_list_page

    html = render_to_string('content/article_list.html', context)

    assert test_list_page['title'] in html

    assert '01 October' in html
    assert '02 October' in html


def test_tag_list_page(context):
    page = {
        'name': 'New to exporting',
        'articles': test_articles,
    }
    context['page'] = page
    html = render_to_string('content/tag_list.html', context)

    assert '01 October' in html
    assert '02 October' in html
    assert 'Article 1 title' in html
    assert 'Article 2 title' in html
    assert 'Articles with tag: New to exporting' in html


def test_landing_page_header_footer(rf, context):
    context['request'] = rf.get('/')

    html = render_to_string('core/landing_page.html', context)

    assert '/static/js/home' in html

    soup = BeautifulSoup(html, 'html.parser')

    assert soup.find(id="great-global-header-logo")


def test_article_detail_page_social_share_links(mock_get_page, client):
    page = {
        "title": "Test article admin title",
        "article_title": "How to write an export plan",
        "article_image": {"url": "foobar.png"},
        "article_body_text": "<p>Lorem ipsum</p>",
        "related_pages": [],
        "full_path": (
            "/advice/create-an-export-plan/how-to-write-an-export-plan/"),
        "last_published_at": "2018-10-09T16:25:13.142357Z",
        "meta": {
            "slug": "how-to-write-an-export-plan",
        },
        "page_type": "ArticlePage",
        "tree_based_breadcrumbs": [
            {"url": "/advice/", "title": "Topic title"},
            {"url": "/advice/create-an-export-plan/", "title": "List title"},
            {"url": (
                "/advice/create-an-export-plan/how-to-write-an-export-plan/"),
                "title": "How to write an export plan"},
        ]
    }

    url = '/advice/create-an-export-plan/how-to-write-an-export-plan/'

    mock_get_page.return_value = create_response(page)

    response = client.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    assert response.status_code == 200
    assert response.template_name == ['content/article_detail.html']

    twitter_link = (
        'https://twitter.com/intent/tweet?text=great.gov.uk'
        '%20-%20How%20to%20write%20an%20export%20plan%20'
        'http://testserver/advice/create-an-export-plan/'
        'how-to-write-an-export-plan/')
    facebook_link = (
        'https://www.facebook.com/share.php?u=http://testserver/'
        'advice/create-an-export-plan/how-to-write-an-export-plan/')
    linkedin_link = (
        'https://www.linkedin.com/shareArticle?mini=true&url='
        'http://testserver/advice/create-an-export-plan/'
        'how-to-write-an-export-plan/&title=great.gov.uk'
        '%20-%20How%20to%20write%20an%20export%20plan%20&source=LinkedIn'
    )
    email_link = (
        'mailto:?body=http://testserver/advice/'
        'create-an-export-plan/how-to-write-an-export-plan/&subject='
        'great.gov.uk%20-%20How%20to%20write%20an%20export%20plan%20'
    )

    assert soup.find(id='share-twitter').attrs['href'] == twitter_link
    assert soup.find(id='share-facebook').attrs['href'] == facebook_link
    assert soup.find(id='share-linkedin').attrs['href'] == linkedin_link
    assert soup.find(id='share-email').attrs['href'] == email_link


def test_article_detail_page_social_share_links_no_title(mock_get_page, client):
    page = {
        "title": "Test article admin title",
        "article_image": {"url": "foobar.png"},
        "article_body_text": "<p>Lorem ipsum</p>",
        "related_pages": [],
        "full_path": (
            "/advice/create-an-export-plan/how-to-write-an-export-plan/"),
        "last_published_at": "2018-10-09T16:25:13.142357Z",
        "meta": {
            "slug": "how-to-write-an-export-plan",
        },
        "page_type": "ArticlePage",
        "tree_based_breadcrumbs": [
            {"url": "/advice/", "title": "Topic title"},
            {"url": "/advice/create-an-export-plan/", "title": "List title"},
            {"url": (
                "/advice/create-an-export-plan/how-to-write-an-export-plan/"),
                "title": "How to write an export plan"},
        ]
    }

    url = '/advice/create-an-export-plan/how-to-write-an-export-plan/'

    mock_get_page.return_value = create_response(page)

    response = client.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    assert response.status_code == 200
    assert response.template_name == ['content/article_detail.html']

    twitter_link = (
        'https://twitter.com/intent/tweet?text=great.gov.uk%20-%20%20'
        'http://testserver/advice/create-an-export-plan/'
        'how-to-write-an-export-plan/')
    linkedin_link = (
        'https://www.linkedin.com/shareArticle?mini=true&url='
        'http://testserver/advice/create-an-export-plan/'
        'how-to-write-an-export-plan/&title=great.gov.uk'
        '%20-%20%20&source=LinkedIn'
    )
    email_link = (
        'mailto:?body=http://testserver/advice/'
        'create-an-export-plan/how-to-write-an-export-plan/&subject='
        'great.gov.uk%20-%20%20'
    )

    assert soup.find(id='share-twitter').attrs['href'] == twitter_link
    assert soup.find(id='share-linkedin').attrs['href'] == linkedin_link
    assert soup.find(id='share-email').attrs['href'] == email_link


def test_country_guide_fact_sheet_displays_if_given_title(rf, context):
    context['request'] = rf.get('/')
    page = {
        'title': 'test',
        'page_type': 'CountryGuidePage',
        'heading': 'Heading',
        'statistics': [],
        'accordions': [],
        'fact_sheet': {
            'fact_sheet_title': 'Fact sheet title',
            'columns': []
        }
    }
    context['page'] = page

    html = render_to_string('content/country_guide.html', context)
    soup = BeautifulSoup(html, 'html.parser')

    assert soup.find(id='country-guide-section-three')
    assert 'Fact sheet title' in html


@pytest.mark.parametrize('intro_ctas', (
    None,
    [],
    [
        {
            'title': 'title 1',
            'link': '',
        }
    ],
    [
        {
            'title': '',
            'link': '',
        }
    ],
))
def test_country_guide_incomplete_intro_ctas(intro_ctas, dummy_cms_page, rf, context):
    context['page'] = dummy_cms_page
    context['request'] = rf.get('/')

    context['page']['heading_teaser'] = 'Teaser'
    context['page']['intro_ctas'] = intro_ctas

    html = render_to_string('content/country_guide.html', context)
    soup = BeautifulSoup(html, 'html.parser')
    ctas = soup.select('#country-guide-teaser-section .intro-cta-link')

    assert len(ctas) == 0


def test_country_guide_complete_intro_ctas(dummy_cms_page, rf, context):
    context['page'] = dummy_cms_page
    context['request'] = rf.get('/')

    intro_ctas = [
        {
            'title': 'title 1',
            'link': 'link 1',
        },
        {
            'title': 'title 2',
            'link': 'link 2',
        },
        {
            'title': 'title 3',
            'link': 'link 3',
        },
    ]

    context['page']['heading_teaser'] = 'Teaser'
    context['page']['intro_ctas'] = intro_ctas

    html = render_to_string('content/country_guide.html', context)
    soup = BeautifulSoup(html, 'html.parser')
    ctas = soup.select('#country-guide-teaser-section .intro-cta-link')

    assert len(ctas) == 3


def test_country_guide_no_intro_ctas(dummy_cms_page, rf, context):
    context['page'] = dummy_cms_page
    context['request'] = rf.get('/')

    context['page']['heading_teaser'] = 'Teaser'

    html = render_to_string('content/country_guide.html', context)
    soup = BeautifulSoup(html, 'html.parser')
    ctas = soup.select('#country-guide-teaser-section .intro-cta-link')

    assert len(ctas) == 0


def test_country_guide_add_href_target(dummy_cms_page, rf, context):
    request = rf.get('/')
    request.META['HTTP_HOST'] = 'example.com'

    context['page'] = dummy_cms_page
    context['request'] = request

    context['page']['section_one_body'] = '<a href="http://www.google.co.uk">Here is an external link</a>'

    html = render_to_string('content/country_guide.html', context)
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.select('#country-guide-section-one a')

    assert len(links) == 1
    assert links[0].attrs['title'] == 'Opens in a new window'
    assert links[0].attrs['target'] == '_blank'
    assert links[0].attrs['rel'] == ['noopener', 'noreferrer']


def test_country_guide_no_industries_no_heading(dummy_cms_page, rf, context):
    context['page'] = dummy_cms_page
    context['request'] = rf.get('/')

    context['page']['accordions'] = []
    context['page']['section_two_heading'] = None

    html = render_to_string('content/country_guide.html', context)
    soup = BeautifulSoup(html, 'html.parser')

    assert not soup.find(id='country-guide-section-two')
    assert not soup.find(id='country-guide-accordions')


def test_country_guide_no_industries(dummy_cms_page, rf, context):
    context['page'] = dummy_cms_page
    context['request'] = rf.get('/')

    context['page']['accordions'] = []
    context['page']['section_two_heading'] = 'Heading'

    html = render_to_string('content/country_guide.html', context)
    soup = BeautifulSoup(html, 'html.parser')

    assert soup.find(id='country-guide-section-two')
    assert not soup.find(id='country-guide-accordions')
