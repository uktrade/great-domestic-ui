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
            reverse('get-finance'),
            {
                'title': 'UK Export Finance - Great.gov.uk',
            },
            200
        ),
        (
            reverse('project-finance'),
            {
                'title': 'UK Export Finance - Project Finance',
            },
            200
        ),
        (
            reverse('uk-export-contact'),
            {
                'title': 'UK Export Finance - Get in touch',
            },
            200
        ),
        (
            reverse('how-we-assess-your-project'),
            {
                'title': 'UK Export Finance - How we assess your project',
            },
            200
        ),
        (
            reverse('what-we-offer-you'),
            {
                'title': 'UK Export Finance - What we offer you',
            },
            200
        ),
        (
            reverse('country-cover'),
            {
                'title': 'UK Export Finance - Check our Country Cover',
            },
            200
        )
    )
)
def test_ukef_views_while_feature_flag_enabled(client, page_url, page_content, expected_status_code, settings):
    response = client.get(page_url)
    assert response.status_code == expected_status_code
    assert page_content['title'] in str(response.rendered_content)


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
            sender={'email_address': 'test@test.com',
                    'country_code': None,
                    'ip_address': None},
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
    request.user = None
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


def test_get_finance_card_bullets(client):
    url = reverse('get-finance')
    response = client.get(url)
    trade_finance_bullets = ['working capital support', 'bond support', 'credit insurance']
    project_finance_bullets = ['UKEF buyer credit guarantees', 'direct lending', 'credit and bond insurance']

    for bullet in trade_finance_bullets:
        assert f'<li>{bullet}</li>' in str(response.content)

    for bullet in project_finance_bullets:
        assert f'<li>{bullet}</li>' in str(response.content)
