from unittest import mock

import pytest
from django.urls import reverse
from django.conf import settings

from ukef import views
from ukef import forms


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
        (
            reverse('project-finance'),
            {
                'title': 'The UK’s Export Credit Agency - great.gov.uk',
            },
            200
        ),
        (
            reverse('uk-export-contact'),
            {
                'title': 'UK Export finance contact form - great.gov.uk',
            },
            200
        ),
        (
            reverse('how-we-assess-your-project'),
            {
                'title': 'How we assess your project - great.gov.uk',
            },
            200
        ),
        (
            reverse('what-we-offer-you'),
            {
                'title': 'What we offer you - great.gov.uk',
            },
            200
        )
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
        (
            reverse('project-finance'),
            404
        ),
        (
            reverse('uk-export-contact'),
            404
        ),
        (
            reverse('how-we-assess-your-project'),
            404
        ),
        (
            reverse('what-we-offer-you'),
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

    # test page redirect if the email doesn't exists in the session
    request.session = {}
    view = views.SuccessPageView.as_view()
    response = view(request)
    assert response.status_code == 302
