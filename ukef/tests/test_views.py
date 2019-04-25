import pytest
from django.urls import reverse


@pytest.mark.parametrize(
    'page_url,page_content,expected_status_code',
    (
        (
            reverse('ukef-get-finance'),
            {
                'title': 'UK Export finance - great.gov.uk',
            },
            200
        ),
    )
)
def test_ukef_views_while_feature_flag_enabled(
    client, page_url, page_content, expected_status_code, settings
):
    settings.FEATURE_FLAGS['UKEF_PAGES_ON'] = True
    response = client.get(page_url)
    assert response.status_code == expected_status_code
    assert page_content['title'] in str(response.rendered_content)


@pytest.mark.parametrize(
    'page_url,expected_status_code',
    (
        (
            reverse('ukef-get-finance'),
            404
        ),
    )
)
def test_ukef_views_while_feature_flag_disabled(
    client, page_url, expected_status_code, settings
):
    settings.FEATURE_FLAGS['UKEF_PAGES_ON'] = False
    response = client.get(page_url)
    assert response.status_code == expected_status_code
