import requests.exceptions
import requests_mock

from contact import helpers

from directory_api_client.client import api_client


def test_retrieve_exporting_advice_email_exception(settings):
    url = api_client.exporting.endpoints['lookup-by-postcode'].format(
        postcode='ABC123'
    )
    with requests_mock.mock() as mock:
        mock.get(url, exc=requests.exceptions.ConnectTimeout)
        email = helpers.retrieve_exporting_advice_email('ABC123')

    assert email == settings.CONTACT_DIT_AGENT_EMAIL_ADDRESS


def test_retrieve_exporting_advice_email_not_ok(settings):
    url = api_client.exporting.endpoints['lookup-by-postcode'].format(
        postcode='ABC123'
    )
    with requests_mock.mock() as mock:
        mock.get(url, status_code=404)
        email = helpers.retrieve_exporting_advice_email('ABC123')

    assert email == settings.CONTACT_DIT_AGENT_EMAIL_ADDRESS


def test_retrieve_exporting_advice_email_success():
    url = api_client.exporting.endpoints['lookup-by-postcode'].format(
        postcode='ABC123'
    )
    match_office = [{'is_match': True, 'email': 'region@example.com'}]
    with requests_mock.mock() as mock:
        mock.get(url, status_code=200, json=match_office)

        email = helpers.retrieve_exporting_advice_email('ABC123')

    assert email == 'region@example.com'


def test_filter_regional_office():

    offices = [
        {'is_match': True, 'email': 'region@example.com'},
        {'is_match': False, 'email': 'region2@example.com'}
    ]

    filtered_office_match = helpers.filter_regional_office(
        matched=True,
        office_list=offices,
    )

    filtered_office_unmatch = helpers.filter_regional_office(
        matched=False,
        office_list=offices,
    )

    assert filtered_office_match == [
        {'is_match': True, 'email': 'region@example.com'}
    ]

    assert filtered_office_unmatch == [
        {'is_match': False, 'email': 'region2@example.com'}
    ]


def test_filter_regional_office_empty():

    filtered_office = helpers.filter_regional_office(
        matched=True,
        office_list=[],
    )

    assert filtered_office is None
