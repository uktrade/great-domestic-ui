from unittest import mock

import pytest

from django.urls import reverse

from core.tests.helpers import create_response
from finance import forms, views


@pytest.fixture(autouse=True)
def company_profile(authed_client):
    path = 'core.mixins.PrepopulateFormMixin.company_profile'
    stub = mock.patch(
        path,
        new_callable=mock.PropertyMock,
        return_value={
            'number': 1234567,
            'name': 'Example corp',
            'postal_code': 'Foo Bar',
            'sectors': ['AEROSPACE'],
            'employees': '1-10',
            'mobile_number': '07171771717',
            'postal_full_name': 'Foo Example',
            'address_line_1': '123 Street',
            'address_line_2': 'Near Fake Town',
            'country': 'FRANCE',
            'locality': 'Paris',
        }
    )
    yield stub.start()
    stub.stop()


@pytest.mark.parametrize(
    'step',
    ('contact', 'your-details', 'company-details', 'help')
)
def test_ukef_lead_generation(client, step):
    url = reverse(
        'uk-export-finance-lead-generation-form', kwargs={'step': step}
    )
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [
        views.GetFinanceLeadGenerationFormView.templates[step]
    ]


@mock.patch('captcha.fields.ReCaptchaField.clean')
@mock.patch('finance.views.PardotAction')
def test_ukef_lead_generation_captcha_revalidation(
    mock_action, mock_clean, client, captcha_stub
):
    url_name = 'uk-export-finance-lead-generation-form'
    view_name = 'get_finance_lead_generation_form_view'

    response = client.post(
        reverse(url_name, kwargs={'step': 'contact'}),
        {
            view_name + '-current_step': 'contact',
            'contact-categories': 'Securing upfront funding',
        }
    )
    assert response.status_code == 302

    response = client.post(
        reverse(url_name, kwargs={'step': 'your-details'}),
        {
            view_name + '-current_step': 'your-details',
            'your-details-firstname': 'test',
            'your-details-lastname': 'test',
            'your-details-position': 'test',
            'your-details-email': 'test@example.com',
            'your-details-phone': 'test',
        }
    )
    assert response.status_code == 302

    response = client.post(
        reverse(url_name, kwargs={'step': 'company-details'}),
        {
            view_name + '-current_step': 'company-details',
            'company-details-trading_name': 'test',
            'company-details-company_number': 'test',
            'company-details-address_line_one': 'test',
            'company-details-address_line_two': 'test',
            'company-details-address_town_city': 'test',
            'company-details-address_county': 'test',
            'company-details-address_post_code': 'test',
            'company-details-industry': 'Other',
            'company-details-industry_other': 'test',
            'company-details-export_status': 'I have customers outside the UK',
        }
    )
    assert response.status_code == 302

    response = client.post(
        reverse(url_name, kwargs={'step': 'help'}),
        {
            view_name + '-current_step': 'help',
            'help-comment': 'test',
            'help-terms_agreed': True,
            'g-recaptcha-response': captcha_stub,
        }
    )
    assert response.status_code == 302

    response = client.get(response.url)

    assert response.status_code == 302
    assert response.url == reverse(
        'uk-export-finance-lead-generation-form-success'
    )
    assert mock_clean.call_count == 1


@mock.patch('finance.views.PardotAction')
def test_ukef_lead_generation_submit(
    mock_action, client, settings, captcha_stub
):
    settings.UKEF_FORM_SUBMIT_TRACKER_URL = 'submit.com'

    view = views.GetFinanceLeadGenerationFormView()

    form_one = forms.CategoryForm(data={
        'categories': ['Securing upfront funding']
    })
    form_two = forms.HelpForm(data={
        'comment': 'thing',
        'terms_agreed': True,
        'g-recaptcha-response': captcha_stub,
    })
    form_three = forms.PersonalDetailsForm(data={
        'firstname': 'Test',
        'lastname': 'Example',
        'position': 'Thing',
        'email': 'test@example.com',
        'phone': '2342'
    })

    assert form_one.is_valid()
    assert form_two.is_valid()
    assert form_three.is_valid()

    response = view.done([form_one, form_two, form_three])

    assert response.status_code == 302
    assert response.url == str(view.success_url)

    assert mock_action.call_count == 1
    assert mock_action.call_args == mock.call(
        pardot_url=settings.UKEF_FORM_SUBMIT_TRACKER_URL,
        form_url=reverse(
            'uk-export-finance-lead-generation-form',
            kwargs={'step': 'contact'}
        ),
        sender={'email_address': 'test@example.com', 'country_code': None}
    )

    assert mock_action().save.call_count == 1
    assert mock_action().save.call_args == mock.call({
        'categories': ['Securing upfront funding'],
        'comment': 'thing',
        'captcha': captcha_stub,
        'firstname': 'Test',
        'lastname': 'Example',
        'position': 'Thing',
        'email': 'test@example.com',
        'phone': '2342',
    })


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_trade_finance_cms(mock_get_finance_page, client, settings):
    settings.UKEF_FORM_SUBMIT_TRACKER_URL = 'submit'
    settings.UKEF_PI_TRACKER_JAVASCRIPT_URL = 'js.com'
    settings.UKEF_PI_TRACKER_ACCOUNT_ID = 'account'
    settings.UKEF_PI_TRACKER_CAMPAIGN_ID = 'campaign'

    url = reverse('get-finance')
    page = {
        'title': 'the page',
        'industries': [{'title': 'good 1'}],
        'meta': {'languages': [['en-gb', 'English']]},
    }
    mock_get_finance_page.return_value = create_response(
        status_code=200,
        json_body=page
    )
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [views.GetFinanceView.template_name]


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_cms_pages_cms_page_404(mock_get, client):
    mock_get.return_value = create_response(status_code=404)

    response = client.get(reverse('get-finance'))

    assert response.status_code == 404


def test_ukef_lead_generation_success_page(client):
    url = reverse('uk-export-finance-lead-generation-form-success')
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [
        views.GetFinanceLeadGenerationSuccessView.template_name
    ]


def test_test_ukef_lead_generationinitial_data(client):
    url_name = 'uk-export-finance-lead-generation-form'

    response_one = client.get(
        reverse(url_name, kwargs={'step': 'your-details'})
    )

    assert response_one.context_data['form'].initial == {
        'email': 'test@foo.com',
        'phone': '07171771717',
        'firstname': 'Foo',
        'lastname': 'Example',
    }

    response_two = client.get(
        reverse(url_name, kwargs={'step': 'company-details'})
    )

    assert response_two.context_data['form'].initial == {
        'not_companies_house': False,
        'company_number': 1234567,
        'trading_name': 'Example corp',
        'industry': 'AEROSPACE',
        'address_line_one': '123 Street',
        'address_line_two': 'Near Fake Town',
        'address_town_city': 'Paris',
        'address_post_code': 'Foo Bar',
    }
