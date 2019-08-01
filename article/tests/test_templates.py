import pytest
from unittest.mock import patch
from bs4 import BeautifulSoup
from django.template.loader import render_to_string

from core.tests.helpers import create_response


@pytest.fixture
def mock_get_page():
    stub = patch(
        'directory_cms_client.client.cms_api_client.lookup_by_slug',
        return_value=create_response(status_code=200)
    )
    yield stub.start()
    stub.stop()


def test_article_detail_page_no_related_content():
    context = {
        'page': {
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
    }

    html = render_to_string('article/article_detail.html', context)
    assert 'Related content' not in html


def test_landing_page_news_section():

    context = {
        'page': {
            'news_title': 'News',
            'news_description': '<p>Lorem ipsum</p>',
            'articles': [
                {'article_title': 'News article 1'},
                {'article_title': 'News article 2'},
            ],
        },
        'features': {'NEWS_SECTION_ON': True}
    }

    html = render_to_string('core/landing_page_domestic.html', context)

    assert context['page']['news_title'] in html
    assert '<p class="body-text">Lorem ipsum</p>' in html
    assert 'News article 1' in html
    assert 'News article 2' in html


def test_article_advice_page(mock_get_page, client, settings):
    context = {}
    page = {
        'title': 'Markets CMS admin title',
        'landing_page_title': 'Markets',
        'hero_image': {'url': 'markets.jpg'},
        'child_pages': [
            {
                'landing_page_title': 'Africa market information',
                'full_path': '/markets/africa/',
                'hero_image': {'url': 'africa.png'},
                'hero_image_thumbnail': {'url': 'africa.jpg'},
                'articles_count': 0,
                'last_published_at': '2018-10-01T15:15:53.927833Z'
            },
            {
                'landing_page_title': 'Asia market information',
                'full_path': '/markets/asia/',
                'hero_image': {'url': 'asia.png'},
                'hero_image_thumbnail': {'url': 'asia.jpg'},
                'articles_count': 3,
                'last_published_at': '2018-10-01T15:16:30.583279Z'
            }
        ],
        "page_type": "TopicLandingPage",
    }

    context['page'] = page

    html = render_to_string('article/topic_list.html', context)

    assert page['title'] not in html
    assert page['landing_page_title'] in html

    assert 'Asia market information' in html
    assert 'Africa market information' not in html
    assert 'markets.jpg' in html
    assert 'asia.jpg' in html
    assert 'africa.jpg' not in html
    assert '01 October 2018' in html


def test_article_detail_page_related_content():
    context = {}
    page = {
        "title": "Test article admin title",
        "article_title": "Test article",
        "article_teaser": "Test teaser",
        "article_image": {"url": "foobar.png"},
        "article_body_text": "<p>Lorem ipsum</p>",
        "related_pages": [
            {
                "article_title": "Related article 1",
                "article_teaser": "Related article 1 teaser",
                "article_image_thumbnail": {"url": "related_article_one.jpg"},
                "full_path": "/markets/test/test-one",
                "meta": {
                    "slug": "test-one",
                }
            },
            {
                "article_title": "Related article 2",
                "article_teaser": "Related article 2 teaser",
                "article_image_thumbnail": {"url": "related_article_two.jpg"},
                "full_path": "/markets/test/test-two",
                "meta": {
                    "slug": "test-two",
                }
            },
        ],
        "full_path": "/markets/foo/bar/",
        "last_published_at": "2018-10-09T16:25:13.142357Z",
        "meta": {
            "slug": "bar",
        },
        "page_type": "ArticlePage",
    }
    context['page'] = page

    html = render_to_string('article/article_detail.html', context)

    assert 'Related content' in html
    soup = BeautifulSoup(html, 'html.parser')

    assert soup.find(
        id='related-article-test-one-link'
    ).attrs['href'] == '/markets/test/test-one'
    assert soup.find(
        id='related-article-test-two-link'
    ).attrs['href'] == '/markets/test/test-two'

    assert soup.find(
        id='related-article-test-one'
    ).select('h3')[0].text == 'Related article 1'
    assert soup.find(
        id='related-article-test-two'
    ).select('h3')[0].text == 'Related article 2'


def test_marketing_article_detail_page_related_content():
    context = {}
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
    context['page'] = page

    html = render_to_string('article/marketing_article_detail.html', context)

    soup = BeautifulSoup(html, 'html.parser')
    assert soup.find(
        id='contact-us-section'
    ).select('h2')[0].text == 'CTA title'

    assert soup.find(
        id='contact-us-section'
    ).select('p')[0].text == 'CTA teaser text'

    assert soup.find(
        id='contact-us-section'
    ).select('a.button')[0].attrs['href'] == 'http://www.great.gov.uk'


def test_marketing_article_detail_page_related_content_not_rendered():
    context = {}
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

    context['page'] = page

    html = render_to_string('article/marketing_article_detail.html', context)

    assert '<section id="contact-us-section"' not in html


def test_marketing_article_detail_content_button_not_rendered_without_link():
    context = {}
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

    context['page'] = page

    html = render_to_string('article/marketing_article_detail.html', context)

    assert 'class="button button-arrow-small"' not in html


test_news_list_page = {
    'title': 'News CMS admin title',
    'landing_page_title': 'News',
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


def test_news_list_page_feature_flag_on():
    context = {
        'features': {'NEWS_SECTION_ON': True}
    }
    context['page'] = test_news_list_page

    html = render_to_string('article/domestic_news_list.html', context)

    assert test_news_list_page['title'] not in html
    assert test_news_list_page['landing_page_title'] in html
    assert 'Lorem ipsum' in html
    assert 'Dolor sit amet' in html


def test_international_news_list_page():
    context = {
        'features': {'NEWS_SECTION_ON': True}
    }
    cms_component = {
        'banner_label': 'Brexit updates',
        'banner_content': '<p>Lorem ipsum.</p>',
        'meta': {'languages': [['en-gb', 'English']]},
    }
    context['page'] = test_news_list_page
    context['cms_component'] = cms_component

    html = render_to_string('article/international_news_list.html', context)

    assert test_news_list_page['title'] not in html
    assert test_news_list_page['landing_page_title'] in html
    assert 'Lorem ipsum' in html
    assert 'Dolor sit amet' in html


def test_domestic_news_article_detail_page():
    context = {
        'features': {'NEWS_SECTION_ON': True}
    }

    page = {
        "title": "Test article admin title",
        "article_title": "Test news title",
        "article_teaser": "Test news teaser",
        "article_image": {"url": "foobar.png"},
        "article_body_text": "<p>Lorem ipsum</p>",
        "related_article_one_url": "",
        "related_article_one_title": "",
        "related_article_one_teaser": "",
        "related_article_two_url": "",
        "related_article_two_title": "",
        "related_article_two_teaser": "",
        "related_article_three_url": "",
        "related_article_three_title": "",
        "related_article_three_teaser": "",
        "full_path": "/markets/foo/bar/",
        "last_published_at": "2018-10-09T16:25:13.142357Z",
        "meta": {
            "slug": "foo",
        },
        "tags": [
            {"name": "Test tag", "slug": "test-tag-slug"}
        ],
        "page_type": "ArticlePage",
    }

    context['page'] = page

    html = render_to_string('article/domestic_news_detail.html', context)

    assert 'Test news title' in html
    assert 'Test news teaser' in html
    assert 'Test tag' not in html
    assert '<p class="body-text">Lorem ipsum</p>' in html


def test_international_news_article_detail_page():
    context = {
        'features': {'NEWS_SECTION_ON': True}
    }

    page = {
        "title": "Test article admin title",
        "article_title": "Test news title",
        "article_teaser": "Test news teaser",
        "article_image": {"url": "foobar.png"},
        "article_body_text": "<p>Lorem ipsum</p>",
        "related_article_one_url": "",
        "related_article_one_title": "",
        "related_article_one_teaser": "",
        "related_article_two_url": "",
        "related_article_two_title": "",
        "related_article_two_teaser": "",
        "related_article_three_url": "",
        "related_article_three_title": "",
        "related_article_three_teaser": "",
        "full_path": "/markets/foo/bar/",
        "last_published_at": "2018-10-09T16:25:13.142357Z",
        "meta": {
            "slug": "foo",
        },
        "page_type": "ArticlePage",
    }
    context['page'] = page

    html = render_to_string('article/international_news_detail.html', context)

    assert 'Test news title' in html
    assert 'Test news teaser' in html
    assert '<p class="body-text">Lorem ipsum</p>' in html


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
    'title': 'List CMS admin title',
    'seo_title': 'SEO title article list',
    'search_description': 'Article list search description',
    'landing_page_title': 'Article list landing page title',
    'hero_image': {'url': 'article_list.png'},
    'hero_teaser': 'Article list hero teaser',
    'list_teaser': '<p>Article list teaser</p>',
    'articles': test_articles,
    'page_type': 'ArticleListingPage',
}


def test_article_list_page():
    context = {}
    context['page'] = test_list_page

    html = render_to_string('article/article_list.html', context)

    assert test_list_page['title'] not in html
    assert test_list_page['landing_page_title'] in html

    assert '01 October' in html
    assert '02 October' in html


def test_tag_list_page():
    context = {}
    page = {
        'name': 'New to exporting',
        'articles': test_articles,
    }
    context['page'] = page
    html = render_to_string('article/tag_list.html', context)

    assert '01 October' in html
    assert '02 October' in html
    assert 'Article 1 title' in html
    assert 'Article 2 title' in html
    assert '2 articles with tag:' in html
    assert 'New to exporting' in html


def test_landing_page_header_footer():

    html = render_to_string('core/landing_page_domestic.html', {})

    assert '/static/js/home' in html

    soup = BeautifulSoup(html, 'html.parser')

    assert soup.find(id="great-global-header-logo")


def test_article_detail_page_social_share_links(
    mock_get_page, client, settings
):
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

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=page
    )

    response = client.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    assert response.status_code == 200
    assert response.template_name == ['article/article_detail.html']

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


def test_article_detail_page_social_share_links_no_title(
    mock_get_page, client, settings
):
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

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=page
    )

    response = client.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    assert response.status_code == 200
    assert response.template_name == ['article/article_detail.html']

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


def test_country_guide_fact_sheet_displays_if_given_title():
    context = {}
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

    html = render_to_string('article/country_guide.html', context)
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
def test_country_guide_incomplete_intro_ctas(intro_ctas, dummy_cms_page):
    context = {
        'page': dummy_cms_page
    }

    context['page']['heading_teaser'] = 'Teaser'
    context['page']['intro_ctas'] = intro_ctas

    html = render_to_string('article/country_guide.html', context)
    soup = BeautifulSoup(html, 'html.parser')
    ctas = soup.select('#country-guide-teaser-section .intro-cta-link')

    assert len(ctas) == 0


def test_country_guide_complete_intro_ctas(dummy_cms_page):
    context = {
        'page': dummy_cms_page
    }

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

    html = render_to_string('article/country_guide.html', context)
    soup = BeautifulSoup(html, 'html.parser')
    ctas = soup.select('#country-guide-teaser-section .intro-cta-link')

    assert len(ctas) == 3


def test_country_guide_no_intro_ctas(dummy_cms_page):
    context = {
        'page': dummy_cms_page
    }

    context['page']['heading_teaser'] = 'Teaser'

    html = render_to_string('article/country_guide.html', context)
    soup = BeautifulSoup(html, 'html.parser')
    ctas = soup.select('#country-guide-teaser-section .intro-cta-link')

    assert len(ctas) == 0
