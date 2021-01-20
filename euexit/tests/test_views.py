from unittest import mock

from django.urls import reverse

from core.constants import CONSENT_EMAIL
from core.tests.helpers import create_response
from euexit import views


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_form_success_page(mock_lookup_by_slug, settings, client):
    url = reverse('brexit-contact-form-success')
    template_name = views.DomesticContactSuccessView.template_name

    mock_lookup_by_slug.return_value = create_response({
        'body_text': 'what next',
        'disclaimer': 'disclaim',
        'breadcrumbs_label': 'Example page',
    })
    settings.FEATURE_FLAGS['HIGH_POTENTIAL_OPPORTUNITIES_ON'] = True
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [template_name]
    assert response.context_data['page'] == {
        'body_text': 'what next',
        'disclaimer': 'disclaim',
        'breadcrumbs_label': 'Example page',
    }
    assert response.context_data['hide_language_selector'] is True


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_domestic_form(mock_lookup_by_slug, client):
    mock_lookup_by_slug.return_value = create_response({
        'disclaimer': 'disclaim',
        'breadcrumbs_label': 'Example page',
    })

    response = client.get(reverse('brexit-contact-form'))

    assert response.status_code == 200
    assert response.template_name == [
        views.DomesticContactFormView.template_name
    ]
    assert response.context_data['hide_language_selector'] is True


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_domestic_form_not_found(mock_lookup_by_slug, client):
    mock_lookup_by_slug.return_value = create_response(status_code=404)

    url = reverse('brexit-contact-form')
    response = client.get(url)

    assert response.status_code == 404


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_domestic_form_cms_retrieval_ok(mock_lookup_by_slug, settings, client):
    settings.FEATURE_FLAGS['HIGH_POTENTIAL_OPPORTUNITIES_ON'] = True
    mock_lookup_by_slug.return_value = create_response({
        'first_name': {
            'label': 'Given name'
        },
        'last_name': {
            'label': 'Family name'
        },
        'disclaimer': 'disclaim',
        'breadcrumbs_label': 'Example page',
    })

    url = reverse('brexit-contact-form')

    response = client.get(url)

    assert response.status_code == 200
    form = response.context_data['form']
    assert form.fields['first_name'].label == 'Given name'
    assert form.fields['last_name'].label == 'Family name'
    assert response.context_data['hide_language_selector'] is True


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@mock.patch.object(views.DomesticContactFormView.form_class, 'save')
def test_domestic_form_submit(
    mock_save, mock_lookup_by_slug, settings, client, captcha_stub
):
    settings.FEATURE_FLAGS['HIGH_POTENTIAL_OPPORTUNITIES_ON'] = True
    settings.EU_EXIT_ZENDESK_SUBDOMAIN = 'brexit-subdomain'
    mock_lookup_by_slug.return_value = create_response({
        'disclaimer': 'disclaim',
        'breadcrumbs_label': 'Example page',
    })

    url = reverse('brexit-contact-form')

    # sets referrer in the session
    client.get(url, {}, HTTP_REFERER='http://www.google.com')
    response = client.post(url, {
        'first_name': 'test',
        'last_name': 'example',
        'email': 'test@example.com',
        'organisation_type': 'COMPANY',
        'company_name': 'thing',
        'comment': 'hello',
        'contact_consent': [CONSENT_EMAIL],
        'g-recaptcha-response': captcha_stub,
    })

    assert response.status_code == 302
    assert response.url == reverse(
        'brexit-contact-form-success'
    )
    assert mock_save.call_count == 1
    assert mock_save.call_args == mock.call(
        subject='Brexit contact form',
        full_name='test example',
        email_address='test@example.com',
        service_name='eu_exit',
        subdomain=settings.EU_EXIT_ZENDESK_SUBDOMAIN,
        form_url=url,
        sender={'email_address': 'test@example.com',
                'country_code': None,
                'ip_address': None}
    )


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_form_urls(mock_lookup_by_slug, client, settings):
    url = reverse('brexit-contact-form')
    settings.FEATURE_FLAGS['HIGH_POTENTIAL_OPPORTUNITIES_ON'] = True
    mock_lookup_by_slug.return_value = create_response({
        'disclaimer': 'disclaim',
        'breadcrumbs_label': 'Example',
    })

    response = client.get(url, {}, HTTP_REFERER='http://www.google.com')

    assert response.status_code == 200
    form = response.context_data['form']
    assert form.ingress_url == 'http://www.google.com'
    assert response.context_data['hide_language_selector'] is True


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_form_url_no_referer(mock_lookup_by_slug, settings, client):
    url = reverse('brexit-contact-form')
    settings.FEATURE_FLAGS['HIGH_POTENTIAL_OPPORTUNITIES_ON'] = True
    mock_lookup_by_slug.return_value = create_response({
        'disclaimer': 'disclaim',
        'breadcrumbs_label': 'Example page',
    })

    response = client.get(url, {})

    assert response.status_code == 200
    form = response.context_data['form']
    assert form.ingress_url is None
    assert response.context_data['hide_language_selector'] is True


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_domestic_prepopulate(mock_lookup_by_slug, client, user):
    mock_lookup_by_slug.return_value = create_response({
        'disclaimer': 'disclaim',
        'breadcrumbs_label': 'Example page',
    })
    url = reverse('brexit-contact-form')
    response = client.get(url)

    assert response.status_code == 200
    assert response.context_data['form'].initial == {
        'email': user.email,
        'company_name': 'Example corp',
        'postcode': 'Foo Bar',
        'first_name': 'Jim',
        'last_name': 'Cross',
        'organisation_type': 'COMPANY',
    }
