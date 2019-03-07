from directory_api_client.client import api_client

from django.conf import settings


def retrieve_exporting_advice_email(postcode):
    try:
        office_details = retrieve_regional_offices(postcode)
        email = filter_regional_office(
            matched=True,
            office_list=office_details
            )[0]['email']
    except Exception:
        email = settings.CONTACT_DIT_AGENT_EMAIL_ADDRESS
    return email


def retrieve_regional_office(postcode):
    office_details = retrieve_regional_offices(postcode)
    return filter_regional_office(
            matched=True,
            office_list=office_details
            )[0]


def retrieve_regional_offices(postcode):
    response = api_client.exporting.lookup_regional_offices_by_postcode(
        postcode
    )
    response.raise_for_status()
    return response.json()


def filter_regional_office(matched, office_list):
    if office_list:
        return list(filter(lambda x: x['is_match'] == matched, office_list))
    else:
        return None
