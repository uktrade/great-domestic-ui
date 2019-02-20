from unittest import mock

from django.conf import settings
from django.urls import reverse

import pytest


def test_form_feature_flag_off(client, settings):
    settings.FEATURE_FLAGS['MARKET_ACCESS_ON'] = False

    response = client.get(reverse('market-access'))

    assert response.status_code == 404


def test_form_feature_flag_on(client, settings):
    settings.FEATURE_FLAGS['MARKET_ACCESS_ON'] = True

    response = client.get(reverse('market-access'))

    assert response.status_code == 200


@pytest.mark.parametrize('status', ['1', '2', '3', '4'])
def test_form_submission_redirects_if_not_option_4_in_current_status(
    client, status
):
    url_name = 'report-ma-barrier'
    view_name = 'report_market_access_barrier_form_view'
    emergency_details_url = '/report-trade-barrier/report/emergency-details/'
    about_url = '/report-trade-barrier/report/about/'

    response = client.post(
        reverse(url_name, kwargs={'step': 'current-status'}),
        {
            view_name + '-current_step': 'current-status',
            'current-status-status': status,
        }
    )

    assert response.status_code == 302
    if status != "4":
        assert response._headers['location'][1] == emergency_details_url
    else:
        assert response._headers['location'][1] == about_url


def test_error_box_at_top_of_page_shows(client):
    url_name = 'report-ma-barrier'
    view_name = 'report_market_access_barrier_form_view'

    response = client.post(
        reverse(url_name, kwargs={'step': 'current-status'}),
        {
            view_name + '-current_step': 'current-status',
            'current-status-status': '',
        }
    )
    assert response.status_code == 200
    assert 'error-message-box' in str(response.content)


@mock.patch('directory_forms_api_client.actions.ZendeskAction')
def test_form_submission(mock_zendesk_action, client):
    url_name = 'report-ma-barrier'
    view_name = 'report_market_access_barrier_form_view'

    response = client.post(
        reverse(url_name, kwargs={'step': 'current-status'}),
        {
            view_name + '-current_step': 'current-status',
            'current-status-status': '4',
        }
    )
    assert response.status_code == 302

    response = client.post(
        reverse(url_name, kwargs={'step': 'about'}),
        {
            view_name + '-current_step': 'about',
            'about-firstname': 'Craig',
            'about-lastname': 'Smith',
            'about-jobtitle': 'Musician',
            'about-categories': "I’m an exporter or I want to export",
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
            'problem-details-country': 'Angola',
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
        'status': '4',
        'firstname': 'Craig',
        'lastname': 'Smith',
        'jobtitle': 'Musician',
        'categories': "I’m an exporter or I want to export",
        'organisation_description': '',
        'company_name': 'Craig Music',
        'email': 'craig@craigmusic.com',
        'phone': '0123456789',
        'product_service': 'something',
        'country': 'Angola',
        'problem_summary': 'problem summary',
        'impact': 'problem impact',
        'resolve_summary': 'steps in resolving',
        'eu_exit_related': 'No',
        'other_details': 'Additional details'
    })


def test_form_initial_data(client):
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
