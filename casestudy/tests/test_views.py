from bs4 import BeautifulSoup
import pytest

from django.core.urlresolvers import reverse

from casestudy import views
import core.helpers


casestudy_views_under_test = [
    (views.CasestudyHelloBabyView, reverse('casestudy-hello-baby')),
    (views.CasestudyYorkBagView, reverse('casestudy-york-bag')),
]


@pytest.mark.parametrize('view_class,url', casestudy_views_under_test)
def test_casestudy_market(client, view_class, url):
    response = client.get(url)
    expected_twitter = core.helpers.build_twitter_link(
        request=response._request, title=view_class.casestudy.title,
    )
    expected_facebook = core.helpers.build_facebook_link(
        request=response._request, title=view_class.casestudy.title,
    )
    expected_linkedin = core.helpers.build_linkedin_link(
        request=response._request, title=view_class.casestudy.title,
    )
    expected_email = core.helpers.build_email_link(
        request=response._request, title=view_class.casestudy.title,
    )
    soup = BeautifulSoup(response.content, 'html.parser')

    assert response.status_code == 200
    assert response.template_name == [view_class.template_name]
    assert response.context_data['casestudy'] == view_class.casestudy
    assert soup.find(id='share-twitter').attrs['href'] == expected_twitter
    assert soup.find(id='share-facebook').attrs['href'] == expected_facebook
    assert soup.find(id='share-linkedin').attrs['href'] == expected_linkedin
    assert soup.find(id='share-email').attrs['href'] == expected_email
