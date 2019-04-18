from unittest import mock

import pytest
from django.urls import reverse

from django.conf import settings
from core.tests.helpers import create_response

from ukef import views
from ukef import forms


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


@mock.patch.object(views.ContactView, 'form_session_class')
@mock.patch.object(forms.UKEFContactForm, 'save')
def test_contact_form_notify_success(
        mock_save, mock_form_session, client, valid_contact_form_data
):
    url = reverse('uk-export-contact')
    response = client.post(url, valid_contact_form_data)

    assert response.status_code == 302
    assert response.url == reverse('uk-export-contract-success')
    assert mock_save.call_count == 2
    assert mock_save.call_args_list == [
        mock.call(
            email_address=settings.UKEF_CONTACT_AGENT_EMAIL_ADDRESS,
            form_session=mock_form_session(),
            form_url=url,
            sender={'email_address': 'test@test.com', 'country_code': None},
            template_id=settings.UKEF_CONTACT_AGENT_NOTIFY_TEMPLATE_ID
        ),
        mock.call(
            email_address='test@test.com',
            form_session=mock_form_session(),
            form_url=url,
            template_id=settings.UKEF_CONTACT_USER_NOTIFY_TEMPLATE_ID
        )
    ]


def test_contact_form_success_view_response(rf):
    user_email = 'test@test.com'
    request = rf.get(reverse('uk-export-contract-success'))
    request.sso_user = None
    request.session = {'user_email': user_email}
    view = views.SuccessPageView.as_view()
    response = view(request)
    assert response.status_code == 200
    assert user_email in response.rendered_content
