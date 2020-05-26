import pytest

from contact import helpers


@pytest.fixture()
def other_offices_formatted():
    return [{
        'address': (
            'The International Trade Centre\n'
            '10 New Street\n'
            'Midlands Business Park\n'
            'Birmingham\n'
            'B20 1RJ'
        ),
        'is_match': False,
        'region_id': 'west_midlands',
        'name': 'DIT West Midlands',
        'address_street': (
            'The International Trade Centre, '
            '10 New Street, '
            'Midlands Business Park'
        ),
        'address_city': 'Birmingham',
        'address_postcode': 'B20 1RJ',
        'email': 'test+west_midlands@examoke.com',
        'phone': '0208 555 4001',
        'phone_other': '',
        'phone_other_comment': '',
        'website': None
        }
    ]


@pytest.fixture()
def all_offices():
    return [{
        'is_match': True,
        'region_id': 'east_midlands',
        'name': 'DIT East Midlands',
        'address_street': (
            'The International Trade Centre, '
            '5 Merus Court, '
            'Meridian Business Park'
        ),
        'address_city': 'Leicester',
        'address_postcode': 'LE19 1RJ',
        'email': 'test+east_midlands@examoke.com',
        'phone': '0345 052 4001',
        'phone_other': '',
        'phone_other_comment': '',
        'website': None
    },
        {
        'is_match': False,
        'region_id': 'west_midlands',
        'name': 'DIT West Midlands',
        'address_street': (
            'The International Trade Centre, '
            '10 New Street, '
            'Midlands Business Park'
        ),
        'address_city': 'Birmingham',
        'address_postcode': 'B20 1RJ',
        'email': 'test+west_midlands@examoke.com',
        'phone': '0208 555 4001',
        'phone_other': '',
        'phone_other_comment': '',
        'website': None
        }
    ]


@pytest.fixture()
def office_formatted():
    return[{
        'address': (
            'The International Trade Centre\n'
            '5 Merus Court\n'
            'Meridian Business Park\n'
            'Leicester\n'
            'LE19 1RJ'
        ),
        'is_match': True,
        'region_id': 'east_midlands',
        'name': 'DIT East Midlands',
        'address_street': (
            'The International Trade Centre, '
            '5 Merus Court, '
            'Meridian Business Park'
        ),
        'address_city': 'Leicester',
        'address_postcode': 'LE19 1RJ',
        'email': 'test+east_midlands@examoke.com',
        'phone': '0345 052 4001',
        'phone_other': '',
        'phone_other_comment': '',
        'website': None
    }]


@pytest.fixture()
def office_unformatted():
    return [{
        'is_match': True,
        'region_id': 'east_midlands',
        'name': 'DIT East Midlands',
        'address_street': (
            'The International Trade Centre, '
            '5 Merus Court, '
            'Meridian Business Park'
        ),
        'address_city': 'Leicester',
        'address_postcode': 'LE19 1RJ',
        'email': 'test+east_midlands@examoke.com',
        'phone': '0345 052 4001',
        'phone_other': '',
        'phone_other_comment': '',
        'website': None
    }]


def test_format_office_details(
        office_formatted,
        office_unformatted,
):
    office = helpers.format_office_details(office_unformatted)
    assert office == office_formatted


def test_format_office_details_empty():
    office = helpers.format_office_details([])
    assert office is None


def test_extract_other_offices_details(all_offices, other_offices_formatted):

    display_offices = helpers.extract_other_offices_details(all_offices)

    assert display_offices == other_offices_formatted


def test_extract_other_offices_details_empty():
    display_offices = helpers.extract_other_offices_details([])
    assert display_offices is None


def test_extract_regional_office_details(all_offices, office_formatted):
    regional_office = helpers.extract_regional_office_details(all_offices)
    assert regional_office == office_formatted[0]


def test_extract_regional_office_details_empty():
    regional_office = helpers.extract_regional_office_details([])
    assert regional_office is None
