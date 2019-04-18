from unittest import mock

import pytest
from django.urls import reverse
from core.tests.helpers import create_response


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
@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_ukef_views_status_code(
        mock_lookup_by_slug, client,
        page_url, page_api_response, expected_status_code
):
    mock_lookup_by_slug.return_value = create_response(
        status_code=200, json_body=page_api_response
    )

    response = client.get(page_url)
    assert response.status_code == expected_status_code
