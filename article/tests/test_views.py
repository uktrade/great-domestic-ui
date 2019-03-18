import pytest
from unittest.mock import call, patch, PropertyMock
from bs4 import BeautifulSoup
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


def test_prototype_landing_page_news_section(mock_get_page, client, settings):
    settings.FEATURE_FLAGS['NEWS_SECTION_ON'] = True

    url = reverse('landing-page')

    page = {
        'news_title': 'News',
        'news_description': '<p>Lorem ipsum</p>',
        'articles': [
            {'article_title': 'News article 1'},
            {'article_title': 'News article 2'},
        ],
    }

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=page
    )
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['article/landing_page.html']

    assert page['news_title'] in str(response.content)
    assert '<p class="body-text">Lorem ipsum</p>' in str(response.content)
    assert 'News article 1' in str(response.content)
    assert 'News article 2' in str(response.content)


test_topic_page = {
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
            'fact_sheet': {'columns': []}
        }
    )

    response = client.get(url)

    assert response.status_code == 200


def test_markets_link_in_header_when_feature_on(
    mock_get_page, client, settings
):
    settings.FEATURE_FLAGS['MARKETS_PAGES_ON'] = True

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body={
            'page_type': 'TopicLandingPage',
        }
    )
    url = reverse('markets')
    response = client.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    assert soup.find(id='header-markets-link')
    assert soup.find(id='header-markets-link').string == 'Markets'


def test_markets_link_not_in_header_when_feature_off(
    mock_get_page, client, settings
):
    settings.FEATURE_FLAGS['MARKETS_PAGES_ON'] = False

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body={
            'page_type': 'TopicLandingPage',
        }
    )
    url = reverse('markets')
    response = client.get(url)

    assert 'id="header-markets-link"' not in str(response.content)


def test_article_advice_page(mock_get_page, client, settings):
    settings.FEATURE_FLAGS['PROTOTYPE_PAGES_ON'] = True

    url = reverse('advice', kwargs={'slug': 'advice'})

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=test_topic_page
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['article/topic_list.html']

    assert test_topic_page['title'] not in str(response.content)
    assert test_topic_page['landing_page_title'] in str(response.content)

    assert 'Asia market information' in str(response.content)
    assert 'Africa market information' not in str(response.content)
    assert 'markets.jpg' in str(response.content)
    assert 'asia.jpg' in str(response.content)
    assert 'africa.jpg' not in str(response.content)
    assert '01 October 2018' in str(response.content)


def test_article_article_detail_page_no_related_content(
    mock_get_page, client, settings
):
    settings.FEATURE_FLAGS['PROTOTYPE_PAGES_ON'] = True

    test_article_page_no_related_content = {
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

    url = reverse(
        'manage-legal-and-ethical-compliance-article',
        kwargs={'slug': 'foo'}
    )

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=test_article_page_no_related_content
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['article/article_detail.html']

    assert 'Related content' not in str(response.content)


def test_article_detail_page_related_content(
    mock_get_page, client, settings
):
    settings.FEATURE_FLAGS['PROTOTYPE_PAGES_ON'] = True

    article_page = {
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

    url = reverse(
        'manage-legal-and-ethical-compliance-article',
        kwargs={'slug': 'foo'}
    )

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=article_page
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['article/article_detail.html']

    assert 'Related content' in str(response.content)
    soup = BeautifulSoup(response.content, 'html.parser')

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


def test_news_list_page_feature_flag_on(mock_get_page, client, settings):
    settings.FEATURE_FLAGS['NEWS_SECTION_ON'] = True

    url = reverse('eu-exit-news-list')

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=test_news_list_page
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['article/domestic_news_list.html']

    assert test_news_list_page['title'] not in str(response.content)
    assert test_news_list_page['landing_page_title'] in str(response.content)
    assert 'Lorem ipsum' in str(response.content)
    assert 'Dolor sit amet' in str(response.content)


@patch('article.views.InternationalNewsListPageView.cms_component',
       new_callable=PropertyMock)
def test_international_news_list_page(
    mock_get_component, mock_get_page, client, settings
):
    settings.FEATURE_FLAGS['NEWS_SECTION_ON'] = True

    url = reverse('international-eu-exit-news-list')

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=test_news_list_page
    )
    mock_get_component.return_value = {
        'banner_label': 'EU exit updates',
        'banner_content': '<p>Lorem ipsum.</p>',
        'meta': {'languages': [['en-gb', 'English']]},
    }

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['article/international_news_list.html']

    assert test_news_list_page['title'] not in str(response.content)
    assert test_news_list_page['landing_page_title'] in str(response.content)
    assert 'Lorem ipsum' in str(response.content)
    assert 'Dolor sit amet' in str(response.content)


def test_domestic_news_article_detail_page(mock_get_page, client, settings):
    settings.FEATURE_FLAGS['NEWS_SECTION_ON'] = True

    test_article_page = {
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

    url = reverse('eu-exit-news-detail', kwargs={'slug': 'foo'})

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=test_article_page
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [
        'article/domestic_news_detail.html']

    assert 'Test news title' in str(response.content)
    assert 'Test news teaser' in str(response.content)
    assert 'Test tag' not in str(response.content)
    assert '<p class="body-text">Lorem ipsum</p>' in str(response.content)


def test_international_news_article_detail_page(
    mock_get_page, client, settings
):
    settings.FEATURE_FLAGS['NEWS_SECTION_ON'] = True

    test_article_page = {
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

    url = reverse('international-eu-exit-news-detail', kwargs={'slug': 'foo'})

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=test_article_page
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [
        'article/international_news_detail.html']

    assert 'Test news title' in str(response.content)
    assert 'Test news teaser' not in str(response.content)
    assert '<p class="body-text">Lorem ipsum</p>' in str(response.content)


def test_news_list_page_feature_flag_off(client, settings):
    settings.FEATURE_FLAGS['NEWS_SECTION_ON'] = False

    url = reverse('eu-exit-news-list')

    response = client.get(url)

    assert response.status_code == 404


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


def test_article_list_page(mock_get_page, client, settings):
    settings.FEATURE_FLAGS['PROTOTYPE_PAGES_ON'] = True

    url = reverse('create-an-export-plan')

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=test_list_page
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['article/article_list.html']

    assert test_list_page['title'] not in str(response.content)
    assert test_list_page['landing_page_title'] in str(response.content)

    assert '01 October' in str(response.content)
    assert '02 October' in str(response.content)


test_tag_page = {
    'name': 'New to exporting',
    'articles': test_articles,
}


@patch('directory_cms_client.client.cms_api_client.lookup_by_tag')
def test_prototype_tag_list_page(mock_get_page, client, settings):
    settings.FEATURE_FLAGS['PROTOTYPE_PAGES_ON'] = True

    url = reverse('tag-list', kwargs={'slug': 'new-to-exporting'})

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=test_tag_page
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['article/tag_list.html']

    assert '01 October' in str(response.content)
    assert '02 October' in str(response.content)
    assert 'Article 1 title' in str(response.content)
    assert 'Article 2 title' in str(response.content)
    assert '2 articles with tag:' in str(response.content)
    assert 'New to exporting' in str(response.content)


def test_landing_page_header_footer(
    mock_get_page, client, settings
):
    settings.FEATURE_FLAGS['PROTOTYPE_PAGES_ON'] = True
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = False

    url = reverse('landing-page')

    page = {
        'news_title': 'News',
        'news_description': '<p>Lorem ipsum</p>',
        'articles': [],
    }

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=page
    )
    response = client.get(url)

    assert response.status_code == 200

    assert '/static/js/home' in str(response.content)
    assert 'Create an export plan' in str(response.content)

    soup = BeautifulSoup(response.content, 'html.parser')

    assert soup.find(id="header-dit-logo")


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


def test_article_detail_page_social_share_links(
    mock_get_page, client, settings
):
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = False

    test_article_page = {
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
    }

    url = reverse(
        'create-an-export-plan-article',
        kwargs={'slug': 'how-to-write-an-export-plan'}
    )

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=test_article_page
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
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = False

    test_article_page = {
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
    }

    url = reverse(
        'create-an-export-plan-article',
        kwargs={'slug': 'how-to-write-an-export-plan'}
    )

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=test_article_page
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
                ]
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
            },
            {
                'link': 'link3'
            }
        ]
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
            },
            {
                'link': 'link3'
            }
        ]
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
            },
            {
                'link': 'link3'
            }
        ]
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
            },
            {
                'link': 'link3'
            }
        ]
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
            },
            {
                'link': 'link2'
            }
        ]
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
