from directory_api_client.client import api_client
import pytest
import requests
import requests_mock

from contact import constants, forms, views


routing_steps = [step for step, _ in views.RoutingFormView.form_list]


@pytest.fixture
def domestic_data(captcha_stub):
    return {
        'given_name': 'Test',
        'family_name': 'Example',
        'email': 'test@example.com',
        'company_type': 'LIMITED',
        'organisation_name': 'Example corp',
        'postcode': 'ABC123',
        'comment': 'Help please',
        'g-recaptcha-response': captcha_stub,
        'terms_agreed': True,
    }


def test_location_form_routing():
    field = forms.LocationRoutingForm.base_fields['choice']
    # for each of the choices the form supports
    for choice, _ in field.choices:
        # the view supports routing the user to that step
        assert choice in routing_steps


def test_domestic_form_routing():
    field = forms.DomesticRoutingForm.base_fields['choice']
    choices = set(item for item, _ in field.choices)

    # expect these choices to result in a redirect to a new form
    choices_expect_redirect = {
        constants.TRADE_OFFICE,
        constants.EXPORT_ADVICE,
        constants.FINANCE,
        constants.EUEXIT,
        constants.EVENTS,
        constants.DSO,
        constants.OTHER,
    }
    mapping = views.RoutingFormView.redirect_mapping[constants.DOMESTIC]

    for choice in choices_expect_redirect:
        assert choice in choices
        assert choice in mapping
        assert choice not in routing_steps

    choices_expect_next_step = (constants.GREAT_SERVICES,)
    for choice in choices_expect_next_step:
        assert choice in choices
        assert choice not in mapping
        assert choice in routing_steps

    expected_choice_count = (
        len(choices_expect_next_step) + len(choices_expect_redirect)
    )

    assert expected_choice_count == len(choices)


def test_great_services_form_routing():
    field = forms.GreatServicesRoutingForm.base_fields['choice']
    choices = set(item for item, _ in field.choices)

    choices_expect_redirect = {
        constants.OTHER,
    }
    mapping = views.RoutingFormView.redirect_mapping[constants.GREAT_SERVICES]

    for choice in choices_expect_redirect:
        assert choice in choices
        assert choice in mapping
        assert choice not in routing_steps

    choices_expect_next_step = {
        constants.EXPORT_OPPORTUNITIES,
        constants.GREAT_ACCOUNT,
    }
    for choice in choices_expect_next_step:
        assert choice in choices
        assert choice not in mapping
        assert choice in routing_steps

    expected_choice_count = (
        len(choices_expect_next_step) + len(choices_expect_redirect)
    )

    assert expected_choice_count == len(choices)


def test_export_opportunities_form_routing():
    field = forms.ExportOpportunitiesRoutingForm.base_fields['choice']

    mapping = (
        views.RoutingFormView.redirect_mapping[constants.EXPORT_OPPORTUNITIES]
    )

    for choice, _ in field.choices:
        assert choice in mapping
        assert choice not in routing_steps


def test_great_account_form_routing():
    # expect these to route to a FAQ page
    pass


def test_international_form_routing():
    field = forms.InternationalRoutingForm.base_fields['choice']
    mapping = views.RoutingFormView.redirect_mapping[constants.INTERNATIONAL]
    for choice, _ in field.choices:
        assert choice in mapping


def test_short_notify_form_serialize_data(domestic_data):
    form = forms.ShortNotifyForm(data=domestic_data)

    assert form.is_valid()

    url = api_client.exporting.endpoints['lookup-by-postcode'].format(
        postcode='ABC123'
    )
    office_details = [
        {'is_match': True, 'name': 'Some Office', 'email': 'foo@example.com'}
    ]
    with requests_mock.mock() as mock:
        mock.get(url, json=office_details)
        data = form.serialized_data

    assert data == {
        'given_name': 'Test',
        'family_name': 'Example',
        'email': 'test@example.com',
        'company_type': 'LIMITED',
        'company_type_other': '',
        'organisation_name': 'Example corp',
        'postcode': 'ABC123',
        'comment': 'Help please',
        'dit_regional_office_name': 'Some Office',
        'dit_regional_office_email': 'foo@example.com',
    }


def test_short_zendesk_form_serialize_data(domestic_data):
    form = forms.ShortZendeskForm(data=domestic_data)

    assert form.is_valid()

    url = api_client.exporting.endpoints['lookup-by-postcode'].format(
        postcode='ABC123'
    )
    office_details = {'name': 'Some Office', 'email': 'foo@example.com'}
    with requests_mock.mock() as mock:
        mock.get(url, json=office_details)
        data = form.serialized_data

    assert data == {
        'given_name': 'Test',
        'family_name': 'Example',
        'email': 'test@example.com',
        'company_type': 'LIMITED',
        'company_type_other': '',
        'organisation_name': 'Example corp',
        'postcode': 'ABC123',
        'comment': 'Help please',
    }
    assert form.full_name == 'Test Example'


def test_domestic_contact_form_serialize_data_office_lookup_error(
    domestic_data
):
    form = forms.ShortNotifyForm(data=domestic_data)

    assert form.is_valid()

    url = api_client.exporting.endpoints['lookup-by-postcode'].format(
        postcode='ABC123'
    )
    with requests_mock.mock() as mock:
        mock.get(url, exc=requests.exceptions.ConnectTimeout)
        data = form.serialized_data

    assert data['dit_regional_office_name'] == ''
    assert data['dit_regional_office_email'] == ''


def test_domestic_contact_form_serialize_data_office_lookup_not_found(
    domestic_data
):
    form = forms.ShortNotifyForm(data=domestic_data)

    assert form.is_valid()

    url = api_client.exporting.endpoints['lookup-by-postcode'].format(
        postcode='ABC123'
    )
    with requests_mock.mock() as mock:
        mock.get(url, status_code=404)
        data = form.serialized_data

    assert data['dit_regional_office_name'] == ''
    assert data['dit_regional_office_email'] == ''


def test_domestic_contact_form_serialize_data_office_lookup_none_returned(
    domestic_data
):
    form = forms.ShortNotifyForm(data=domestic_data)

    assert form.is_valid()

    url = api_client.exporting.endpoints['lookup-by-postcode'].format(
        postcode='ABC123'
    )
    with requests_mock.mock() as mock:
        mock.get(url, json=None)

    data = form.serialized_data

    assert data['dit_regional_office_name'] == ''
    assert data['dit_regional_office_email'] == ''


def test_feedback_form_serialize_data(captcha_stub):
    form = forms.FeedbackForm(
        data={
            'name': 'Test Example',
            'email': 'test@example.com',
            'comment': 'Help please',
            'g-recaptcha-response': captcha_stub,
            'terms_agreed': True,
        }
    )

    assert form.is_valid()
    assert form.serialized_data == {
        'name': 'Test Example',
        'email': 'test@example.com',
        'comment': 'Help please',
    }
    assert form.full_name == 'Test Example'


@pytest.mark.parametrize('form_class,value', (
    (forms.InternationalRoutingForm, True),
    (forms.InternationalRoutingForm, False),
))
def test_routing_forms_feature_flag(form_class, value, feature_flags):
    expected = constants.EXPORTING_TO_UK
    feature_flags['EXPORTING_TO_UK_ON'] = value

    choices = form_class().fields['choice'].choices
    assert any(item == expected for item, _ in choices) is value


@pytest.mark.parametrize('value', (True, False,))
def test_routing_forms_new_reg_journey_flag(value, feature_flags):
    feature_flags['NEW_REGISTRATION_JOURNEY_ON'] = value

    choices = forms.GreatAccountRoutingForm().fields['choice'].choices

    assert any(
        value == constants.COMPANY_NOT_FOUND for value,
        label in choices
    ) is value


def test_selling_online_overseas_business_valid_form_soletrader():
    form = forms.SellingOnlineOverseasBusiness(
        data={
            'company_name': 'Acme',
            'soletrader': True,
            'company_postcode': 'SW1H 0TL',
            'website_address': 'bar'
        }
    )
    assert form.is_valid()


def test_selling_online_overseas_business_valid_form_company():
    form = forms.SellingOnlineOverseasBusiness(
        data={
            'company_name': 'Acme',
            'company_number': '123',
            'company_postcode': 'SW1H 0TL',
            'website_address': 'bar'
        }
    )
    assert form.is_valid()


def test_selling_online_overseas_business_invalid_form():
    form = forms.SellingOnlineOverseasBusiness(
        data={
            'company_name': 'Acme',
            'company_postcode': 'SW1H 0TL',
            'website_address': 'bar'
        }
    )
    assert form.is_valid() is False
    assert form.errors == {'company_number': ['This field is required.']}


@pytest.mark.parametrize('value', (True, False,))
def test_routing_forms_capital_invest_feature_flag(value, feature_flags):
    feature_flags['CAPITAL_INVEST_CONTACT_IN_TRIAGE_ON'] = value
    choices = forms.InternationalRoutingForm().fields['choice'].choices

    assert any(value == constants.CAPITAL_INVEST for value, label in choices) is value
