import pytest
from django.urls import reverse


@pytest.mark.parametrize(
    'view_name,expected_url',
    (
        (
            'landing-page', '/'
        ),
        (
            'not-found',
            '/not-found/'
        ),
        (
            'privacy-and-cookies',
            '/privacy-and-cookies/'
        ),
        (
            'terms-and-conditions',
            '/terms-and-conditions/'
        ),
        (
            'get-finance',
            '/get-finance/'
        )
    )
)
def test_reverse_urls(view_name, expected_url):
    assert reverse(view_name) == expected_url
