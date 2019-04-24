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
    )
)
def test_ukef_views_status_code(
    client, page_url, page_api_response, expected_status_code
):
    response = client.get(page_url)
    assert response.status_code == expected_status_code
