from unittest import mock

from django.conf import settings
from django.urls import reverse

from marketing import forms, views


@mock.patch.object(views.MarketingJoinFormPageView, 'form_session_class')
@mock.patch.object(forms.MarketingJoinForm, 'save')
def test_marketing_join_form_notify_success(
    mock_save, mock_form_session, client, valid_marketing_form_data
):
    url = reverse('marketing-join-form')
    response = client.post(url, valid_marketing_form_data)

    assert response.status_code == 302
    assert response.url == reverse('marketing-join-success')
    assert mock_save.call_count == 2
    assert mock_save.call_args_list == [
        mock.call(
            email_address=settings.COMMUNITY_ENQUIRIES_AGENT_EMAIL_ADDRESS,
            form_session=mock_form_session(),
            form_url=url,
            sender={'email_address': 'test@test.com', 'country_code': None},
            template_id=settings.COMMUNITY_ENQUIRIES_AGENT_NOTIFY_TEMPLATE_ID
        ),
        mock.call(
            email_address='test@test.com',
            form_session=mock_form_session(),
            form_url=url,
            template_id=settings.COMMUNITY_ENQUIRIES_USER_NOTIFY_TEMPLATE_ID
        )
    ]


def test_marketing_success_view(client):
    url = reverse('marketing-join-success')

    response = client.get(url)

    assert response.status_code == 200
