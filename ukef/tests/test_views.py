import pytest
from django.urls import reverse


@pytest.mark.parametrize(
    'page_url,page_api_response,expected_status_code',
    (
        (
            reverse('get-finance'),
            {
                'title': 'UK EXPORT FINANCE',
                'meta': {
                    'slug': 'get-finance'
                }
            },
            200
        ),
        (
            reverse('project-finance'),
            {
                'title': 'UKEF LANDING',
                'meta': {
                    'slug': 'project-finance'
                }
            },
            200
        ),
        (
            reverse('uk-export-contact'),
            {
                'title': 'Get in touch',
                'meta': {
                    'slug': 'uk-export-contact-form'
                }
            },
            200
        ),
        (
            reverse('uk-export-contract-success'),
            {
                'title': 'Get in touch Success',
                'meta': {
                    'slug': 'uk-export-contact-form-success'
                }
            },
            302
        ),
        (
            reverse('how-we-assess-your-project'),
            {
                'title': 'How we assess your project',
                'meta': {
                    'slug': 'how-we-assess-your-project'
                }
            },
            200
        ),
        (
            reverse('country-cover'),
            {
                'title': 'Country Cover',
                'meta': {
                    'slug': 'country-cover'
                }
            },
            200
        ),
        (
            reverse('what-we-offer-you'),
            {
                'title': 'What we offer you',
                'meta': {
                    'slug': 'what-we-offer-you'
                }
            },
            200
        ),

    )
)
def test_ukef_views_status_code(
        page_url, page_api_response, expected_status_code, client
):
    response = client.get(page_url)
    assert response.status_code == expected_status_code
