from unittest import mock

from django.conf import settings
from django.urls import reverse


def test_form_feature_flag_off(client, settings):
    settings.FEATURE_FLAGS['MARKET_ACCESS_ON'] = False

    response = client.get(reverse('market-access'))

    assert response.status_code == 404


def test_form_feature_flag_on(client, settings):
    settings.FEATURE_FLAGS['MARKET_ACCESS_ON'] = True

    response = client.get(reverse('market-access'))

    assert response.status_code == 200


def test_error_box_at_top_of_page_shows(client):
    settings.FEATURE_FLAGS['MARKET_ACCESS_ON'] = True
    url_name = 'report-ma-barrier'
    view_name = 'report_market_access_barrier_form_view'

    response = client.post(
        reverse(url_name, kwargs={'step': 'about'}),
        {
            view_name + '-current_step': 'about',
            'about-firstname': '',
            'about-lastname': '',
            'about-jobtitle': '',
            'about-business_type': '',
            'about-company_name': '',
            'about-email': '',
            'about-phone': '',
        }
    )
    assert response.status_code == 200
    assert 'error-message-box' in str(response.content)


@mock.patch('directory_forms_api_client.actions.ZendeskAction')
def test_form_submission(mock_zendesk_action, client):
    settings.FEATURE_FLAGS['MARKET_ACCESS_ON'] = True
    url_name = 'report-ma-barrier'
    view_name = 'report_market_access_barrier_form_view'
    business_type = ("I’m an exporter or investor, or "
                     "I want to export or invest")

    response = client.post(
        reverse(url_name, kwargs={'step': 'about'}),
        {
            view_name + '-current_step': 'about',
            'about-firstname': 'Craig',
            'about-lastname': 'Smith',
            'about-jobtitle': 'Musician',
            'about-business_type': business_type,
            'about-company_name': 'Craig Music',
            'about-email': 'craig@craigmusic.com',
            'about-phone': '0123456789',
        }
    )
    assert response.status_code == 302

    response = client.post(
        reverse(url_name, kwargs={'step': 'problem-details'}),
        {
            view_name + '-current_step': 'problem-details',
            'problem-details-product_service': 'something',
            'problem-details-location': 'Angola',
            'problem-details-problem_summary': 'problem summary',
            'problem-details-impact': 'problem impact',
            'problem-details-resolve_summary': 'steps in resolving',
            'problem-details-eu_exit_related': 'No',

        }
    )
    assert response.status_code == 302

    response = client.post(
        reverse(url_name, kwargs={'step': 'other-details'}),
        {
            view_name + '-current_step': 'other-details',
            'other-details-other_details': 'Additional details'
        }
    )
    assert response.status_code == 302

    response = client.post(
        reverse(url_name, kwargs={'step': 'summary'}),
        {
            view_name + '-current_step': 'summary',
        }
    )
    assert response.status_code == 302
    assert response.url == reverse(url_name, kwargs={'step': 'finished'})

    response = client.get(response.url)

    assert response.status_code == 200

    assert mock_zendesk_action.call_count == 1
    subject = f"{settings.MARKET_ACCESS_ZENDESK_SUBJECT}: Angola: Craig Music"
    assert mock_zendesk_action.call_args == mock.call(
        subject=subject,
        full_name='Craig Smith',
        email_address='craig@craigmusic.com',
        service_name='market_access',
        form_url=reverse(url_name, kwargs={'step': 'about'}),
        sender={'email_address': 'craig@craigmusic.com', 'country_code': None},
    )
    assert mock_zendesk_action().save.call_count == 1
    assert mock_zendesk_action().save.call_args == mock.call({
        'firstname': 'Craig',
        'lastname': 'Smith',
        'jobtitle': 'Musician',
        'business_type': business_type,
        'other_business_type': '',
        'company_name': 'Craig Music',
        'email': 'craig@craigmusic.com',
        'phone': '0123456789',
        'product_service': 'something',
        'location': 'Angola',
        'problem_summary': 'problem summary',
        'impact': 'problem impact',
        'resolve_summary': 'steps in resolving',
        'eu_exit_related': 'No',
        'other_details': 'Additional details'
    })


def test_form_initial_data(client):
    settings.FEATURE_FLAGS['MARKET_ACCESS_ON'] = True
    response_one = client.get(
        reverse('report-ma-barrier', kwargs={'step': 'about'}),
    )
    assert response_one.context_data['form'].initial == {}

    response_two = client.get(
        reverse('report-ma-barrier', kwargs={'step': 'problem-details'}),
    )
    assert response_two.context_data['form'].initial == {}

    response_four = client.get(
        reverse('report-ma-barrier', kwargs={'step': 'other-details'}),
    )
    assert response_four.context_data['form'].initial == {}
