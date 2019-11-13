from unittest import mock

from directory_api_client.exporting import url_lookup_by_postcode
from directory_forms_api_client.helpers import Sender

from directory_constants import slugs
import pytest
import requests_mock

import django.forms
from django.conf import settings
from django.core.cache import cache
from django.urls import reverse

from contact import constants, forms, views
from core.tests.helpers import create_response, reload_urlconf


def build_wizard_url(step):
    return reverse('contact-us-routing-form', kwargs={'step': step})


class ChoiceForm(django.forms.Form):
    choice = django.forms.CharField()


@pytest.fixture()
def all_office_details():
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


@pytest.fixture
def domestic_form_data(captcha_stub):
    return {
        'given_name': 'Test',
        'family_name': 'Example',
        'email': 'test@example.com',
        'company_type': 'LIMITED',
        'organisation_name': 'Example corp',
        'postcode': '**** ***',
        'comment': 'Help please',
        'g-recaptcha-response': captcha_stub,
        'terms_agreed': True,
    }


@pytest.mark.parametrize('current_step,choice,expected_url', (
    # location step routing
    (
        constants.LOCATION,
        constants.DOMESTIC,
        build_wizard_url(constants.DOMESTIC),
    ),
    (
        constants.LOCATION,
        constants.INTERNATIONAL,
        build_wizard_url(constants.INTERNATIONAL),
    ),
    # domestic step routing
    (
        constants.DOMESTIC,
        constants.TRADE_OFFICE,
        reverse('office-finder'),
    ),
    (
        constants.DOMESTIC,
        constants.EXPORT_ADVICE,
        reverse(
            'contact-us-export-advice',
            kwargs={'step': 'comment'}
        ),
    ),
    (
        constants.DOMESTIC,
        constants.FINANCE,
        reverse(
            'uk-export-finance-lead-generation-form',
            kwargs={'step': 'contact'},
        )
    ),
    (
        constants.DOMESTIC,
        constants.EUEXIT,
        reverse('brexit-contact-form'),
    ),
    (
        constants.DOMESTIC,
        constants.EVENTS,
        reverse('contact-us-events-form'),
    ),
    (
        constants.DOMESTIC,
        constants.DSO,
        reverse('contact-us-dso-form')
    ),
    (
        constants.DOMESTIC,
        constants.OTHER,
        reverse('contact-us-enquiries')
    ),
    # great services guidance routing
    (
        constants.GREAT_SERVICES,
        constants.EXPORT_OPPORTUNITIES,
        build_wizard_url(constants.EXPORT_OPPORTUNITIES),
    ),
    (
        constants.GREAT_SERVICES,
        constants.GREAT_ACCOUNT,
        build_wizard_url(constants.GREAT_ACCOUNT),
    ),
    (
        constants.GREAT_SERVICES,
        constants.OTHER,
        reverse('contact-us-domestic'),
    ),
    # great account
    (
        constants.GREAT_ACCOUNT,
        constants.NO_VERIFICATION_EMAIL,
        views.build_account_guidance_url(slugs.HELP_MISSING_VERIFY_EMAIL),
    ),
    (
        constants.GREAT_ACCOUNT,
        constants.COMPANY_NOT_FOUND,
        views.build_account_guidance_url(slugs.HELP_ACCOUNT_COMPANY_NOT_FOUND),
    ),
    (
        constants.GREAT_ACCOUNT,
        constants.PASSWORD_RESET,
        views.build_account_guidance_url(slugs.HELP_PASSWORD_RESET),
    ),
    (
        constants.GREAT_ACCOUNT,
        constants.COMPANIES_HOUSE_LOGIN,
        views.build_account_guidance_url(slugs.HELP_COMPANIES_HOUSE_LOGIN),
    ),
    (
        constants.GREAT_ACCOUNT,
        constants.VERIFICATION_CODE,
        views.build_account_guidance_url(slugs.HELP_VERIFICATION_CODE_ENTER),
    ),
    (
        constants.GREAT_ACCOUNT,
        constants.NO_VERIFICATION_LETTER,
        views.build_account_guidance_url(slugs.HELP_VERIFICATION_CODE_LETTER),
    ),
    (
        constants.GREAT_ACCOUNT,
        constants.NO_VERIFICATION_MISSING,
        views.build_account_guidance_url(slugs.HELP_VERIFICATION_CODE_MISSING),
    ),
    (
        constants.GREAT_ACCOUNT,
        constants.OTHER,
        reverse('contact-us-domestic'),
    ),
    # Export opportunities guidance routing
    (
        constants.EXPORT_OPPORTUNITIES,
        constants.NO_RESPONSE,
        views.build_export_opportunites_guidance_url(
            slugs.HELP_EXOPPS_NO_RESPONSE
        ),
    ),
    (
        constants.EXPORT_OPPORTUNITIES,
        constants.ALERTS,
        views.build_export_opportunites_guidance_url(
            slugs.HELP_EXOPP_ALERTS_IRRELEVANT
        ),
    ),
    (
        constants.EXPORT_OPPORTUNITIES,
        constants.OTHER,
        reverse('contact-us-domestic'),
    ),
    # international routing
    (
        constants.INTERNATIONAL,
        constants.INVESTING,
        settings.INVEST_CONTACT_URL,
    ),
    (
        constants.INTERNATIONAL,
        constants.EXPORTING_TO_UK,
        views.build_exporting_guidance_url(slugs.HELP_EXPORTING_TO_UK)
    ),
    (
        constants.INTERNATIONAL,
        constants.BUYING,
        settings.FIND_A_SUPPLIER_CONTACT_URL,
    ),
    (
        constants.INTERNATIONAL,
        constants.OTHER,
        reverse('contact-us-international'),
    ),
    # exporting to the UK routing
    (
        constants.EXPORTING_TO_UK,
        constants.HMRC,
        settings.CONTACT_EXPORTING_TO_UK_HMRC_URL,
    ),
    (
        constants.EXPORTING_TO_UK,
        constants.DEFRA,
        reverse('contact-us-exporting-to-the-uk-defra')
    ),
    (
        constants.EXPORTING_TO_UK,
        constants.BEIS,
        reverse('contact-us-exporting-to-the-uk-beis')
    ),
    (
        constants.EXPORTING_TO_UK,
        constants.IMPORT_CONTROLS,
        reverse('contact-us-international')
    ),
    (
        constants.EXPORTING_TO_UK,
        constants.TRADE_WITH_UK_APP,
        reverse('contact-us-international')
    ),
    (
        constants.EXPORTING_TO_UK,
        constants.OTHER,
        reverse('contact-us-international'),
    )
))
def test_render_next_step(current_step, choice, expected_url):
    form = ChoiceForm(data={'choice': choice})

    view = views.RoutingFormView()
    view.steps = mock.Mock(current=current_step)
    view.storage = mock.Mock()
    view.url_name = 'contact-us-routing-form'
    view.request = mock.Mock()
    view.form_session = mock.Mock()

    assert form.is_valid()
    assert view.render_next_step(form).url == expected_url


@pytest.mark.parametrize('current_step,expected_step', (
    (constants.DOMESTIC, constants.LOCATION),
    (constants.INTERNATIONAL, constants.LOCATION),
    (constants.GREAT_SERVICES, constants.DOMESTIC),
    (constants.GREAT_ACCOUNT, constants.GREAT_SERVICES),
    (constants.EXPORT_OPPORTUNITIES, constants.GREAT_SERVICES),
))
def test_get_previous_step(current_step, expected_step):
    view = views.RoutingFormView()
    view.steps = mock.Mock(current=current_step)
    view.storage = mock.Mock()
    view.url_name = 'contact-us-routing-form'

    assert view.get_prev_step() == expected_step


@pytest.mark.parametrize(
    'url,success_url,view_class,agent_template,user_template,agent_email',
    (
        (
            reverse('contact-us-events-form'),
            reverse('contact-us-events-success'),
            views.EventsFormView,
            settings.CONTACT_EVENTS_AGENT_NOTIFY_TEMPLATE_ID,
            settings.CONTACT_EVENTS_USER_NOTIFY_TEMPLATE_ID,
            settings.CONTACT_EVENTS_AGENT_EMAIL_ADDRESS,
        ),
        (
            reverse('contact-us-dso-form'),
            reverse('contact-us-dso-success'),
            views.DefenceAndSecurityOrganisationFormView,
            settings.CONTACT_DSO_AGENT_NOTIFY_TEMPLATE_ID,
            settings.CONTACT_DSO_USER_NOTIFY_TEMPLATE_ID,
            settings.CONTACT_DSO_AGENT_EMAIL_ADDRESS,
        ),
        (
            reverse('contact-us-international'),
            reverse('contact-us-international-success'),
            views.InternationalFormView,
            settings.CONTACT_INTERNATIONAL_AGENT_NOTIFY_TEMPLATE_ID,
            settings.CONTACT_INTERNATIONAL_USER_NOTIFY_TEMPLATE_ID,
            settings.CONTACT_INTERNATIONAL_AGENT_EMAIL_ADDRESS,
        ),
        (
            reverse('office-finder-contact', kwargs={'postcode': 'FOO'}),
            reverse('contact-us-office-success', kwargs={'postcode': 'FOO'}),
            views.OfficeContactFormView,
            settings.CONTACT_OFFICE_AGENT_NOTIFY_TEMPLATE_ID,
            settings.CONTACT_OFFICE_USER_NOTIFY_TEMPLATE_ID,
            settings.CONTACT_DIT_AGENT_EMAIL_ADDRESS,
        ),
        (
            reverse('contact-us-exporting-to-the-uk-beis'),
            reverse('contact-us-exporting-to-the-uk-beis-success'),
            views.ExportingToUKBEISFormView,
            settings.CONTACT_BEIS_AGENT_NOTIFY_TEMPLATE_ID,
            settings.CONTACT_BEIS_USER_NOTIFY_TEMPLATE_ID,
            settings.CONTACT_BEIS_AGENT_EMAIL_ADDRESS,
        ),
        (
            reverse('contact-us-exporting-to-the-uk-defra'),
            reverse('contact-us-exporting-to-the-uk-defra-success'),
            views.ExportingToUKDERAFormView,
            settings.CONTACT_DEFRA_AGENT_NOTIFY_TEMPLATE_ID,
            settings.CONTACT_DEFRA_USER_NOTIFY_TEMPLATE_ID,
            settings.CONTACT_DEFRA_AGENT_EMAIL_ADDRESS,
        )
    )
)
@mock.patch.object(views.FormSessionMixin, 'form_session_class')
def test_notify_form_submit_success(
    mock_form_session, client, url, agent_template, user_template,
    view_class, agent_email, success_url, settings
):

    class Form(forms.SerializeDataMixin, django.forms.Form):
        email = django.forms.EmailField()
        save = mock.Mock()

    with mock.patch.object(view_class, 'form_class', Form):
        response = client.post(url, {'email': 'test@example.com'})

    assert response.status_code == 302
    assert response.url == success_url

    assert Form.save.call_count == 2
    assert Form.save.call_args_list == [
        mock.call(
            template_id=agent_template,
            email_address=agent_email,
            form_url=url,
            form_session=mock_form_session(),
            sender={'email_address': 'test@example.com', 'country_code': None}
        ),
        mock.call(
            template_id=user_template,
            email_address='test@example.com',
            form_url=url,
            form_session=mock_form_session(),
        )
    ]


@pytest.mark.parametrize('url,slug', (
    (
        reverse('contact-us-events-success'),
        slugs.HELP_FORM_SUCCESS_EVENTS,
    ),
    (
        reverse('contact-us-dso-success'),
        slugs.HELP_FORM_SUCCESS_DSO,
    ),
    (
        reverse('contact-us-export-advice-success'),
        slugs.HELP_FORM_SUCCESS_EXPORT_ADVICE,
    ),
    (
        reverse('contact-us-feedback-success'),
        slugs.HELP_FORM_SUCCESS_FEEDBACK,
    ),
    (
        reverse('contact-us-domestic-success'),
        slugs.HELP_FORM_SUCCESS,
    ),
    (
        reverse('contact-us-international-success'),
        slugs.HELP_FORM_SUCCESS_INTERNATIONAL,
    ),
    (
        reverse('contact-us-office-success', kwargs={'postcode': 'FOOBAR'}),
        slugs.HELP_FORM_SUCCESS,
    ),
    (
        reverse('contact-us-exporting-to-the-uk-beis-success'),
        slugs.HELP_FORM_SUCCESS_BEIS,
    ),
    (
        reverse('contact-us-exporting-to-the-uk-defra-success'),
        slugs.HELP_FORM_SUCCESS_DEFRA,
    )

))
@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_success_view_cms(mock_lookup_by_slug, url, slug, client):
    mock_lookup_by_slug.return_value = create_response()

    response = client.get(url)

    assert response.status_code == 200
    assert mock_lookup_by_slug.call_count == 1
    assert mock_lookup_by_slug.call_args == mock.call(
        draft_token=None, language_code='en-gb', slug=slug
    )


@mock.patch('captcha.fields.ReCaptchaField.clean')
@mock.patch('directory_forms_api_client.actions.GovNotifyEmailAction')
@mock.patch('directory_forms_api_client.actions.EmailAction')
@mock.patch('contact.helpers.retrieve_exporting_advice_email')
@mock.patch.object(views.FormSessionMixin, 'form_session_class')
def test_exporting_from_uk_contact_form_submission(
    mock_form_session, mock_retrieve_exporting_advice_email, mock_email_action,
    mock_notify_action, mock_clean, client, captcha_stub, company_profile,
    settings
):
    company_profile.return_value = create_response(status_code=404)
    mock_retrieve_exporting_advice_email.return_value = 'regional@example.com'

    url_name = 'contact-us-export-advice'
    view_name = 'exporting_advice_form_view'

    response = client.post(
        reverse(url_name, kwargs={'step': 'comment'}),
        {
            view_name + '-current_step': 'comment',
            'comment-comment': 'some comment',
        }
    )
    assert response.status_code == 302

    response = client.post(
        reverse(url_name, kwargs={'step': 'personal'}),
        {
            view_name + '-current_step': 'personal',
            'personal-first_name': 'test',
            'personal-last_name': 'test',
            'personal-position': 'test',
            'personal-email': 'test@example.com',
            'personal-phone': 'test',
        }
    )

    assert response.status_code == 302

    response = client.post(
        reverse(url_name, kwargs={'step': 'business'}),
        {
            view_name + '-current_step': 'business',
            'business-company_type': 'LIMITED',
            'business-companies_house_number': '12345678',
            'business-organisation_name': 'Example corp',
            'business-postcode': '1234',
            'business-industry': 'AEROSPACE',
            'business-turnover': '0-25k',
            'business-employees': '1-10',
            'business-captcha': captcha_stub,
            'business-terms_agreed': True,
        }
    )
    assert response.status_code == 302

    response = client.get(response.url)

    assert response.status_code == 302
    assert response.url == reverse('contact-us-domestic-success')
    assert mock_clean.call_count == 1
    assert mock_notify_action.call_count == 1
    assert mock_notify_action.call_args == mock.call(
        template_id=settings.CONTACT_EXPORTING_USER_NOTIFY_TEMPLATE_ID,
        email_address='test@example.com',
        form_url='/contact/export-advice/comment/',
        form_session=mock_form_session(),
        email_reply_to_id=settings.CONTACT_EXPORTING_USER_REPLY_TO_EMAIL_ID
    )
    assert mock_notify_action().save.call_count == 1
    assert mock_notify_action().save.call_args == mock.call({
        'comment': 'some comment',
        'first_name': 'test',
        'last_name': 'test',
        'position': 'test',
        'email': 'test@example.com',
        'phone': 'test',
        'company_type': 'LIMITED',
        'companies_house_number': '12345678',
        'company_type_other': '',
        'organisation_name': 'Example corp',
        'postcode': '1234',
        'industry': 'AEROSPACE',
        'industry_other': '',
        'turnover': '0-25k',
        'employees': '1-10',
        'region_office_email': 'regional@example.com',
    })

    assert mock_email_action.call_count == 1
    assert mock_email_action.call_args == mock.call(
        recipients=['regional@example.com'],
        subject=settings.CONTACT_EXPORTING_AGENT_SUBJECT,
        reply_to=[settings.DEFAULT_FROM_EMAIL],
        form_url='/contact/export-advice/comment/',
        form_session=mock_form_session(),
        sender={'email_address': 'test@example.com', 'country_code': None}
    )
    assert mock_email_action().save.call_count == 1
    assert mock_email_action().save.call_args == mock.call({
        'text_body': mock.ANY, 'html_body': mock.ANY
    })

    assert mock_retrieve_exporting_advice_email.call_count == 1
    assert mock_retrieve_exporting_advice_email.call_args == mock.call(
        '1234'
    )


@mock.patch('captcha.fields.ReCaptchaField.clean')
@mock.patch('directory_forms_api_client.actions.GovNotifyEmailAction')
@mock.patch('directory_forms_api_client.actions.EmailAction')
@mock.patch('contact.helpers.retrieve_exporting_advice_email')
def test_exporting_from_uk_contact_form_initial_data_business(
    mock_retrieve_exporting_advice_email, mock_email_action,
    mock_notify_action, mock_clean, client, captcha_stub, user
):
    mock_retrieve_exporting_advice_email.return_value = 'regional@example.com'

    url_name = 'contact-us-export-advice'

    response_one = client.get(reverse(url_name, kwargs={'step': 'personal'}))

    assert response_one.context_data['form'].initial == {
        'email': user.email,
        'phone': '55512345',
        'first_name': 'Jim',
        'last_name': 'Cross',
    }

    response_two = client.get(reverse(url_name, kwargs={'step': 'business'}))

    assert response_two.context_data['form'].initial == {
        'company_type': forms.LIMITED,
        'companies_house_number': 1234567,
        'organisation_name': 'Example corp',
        'postcode': 'Foo Bar',
        'industry': 'AEROSPACE',
        'employees': '1-10',
    }


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_guidance_view_cms_retrieval(mock_lookup_by_slug, client):
    mock_lookup_by_slug.return_value = create_response()

    url = reverse(
        'contact-us-export-opportunities-guidance', kwargs={'slug': 'the-slug'}
    )

    response = client.get(url)

    assert response.status_code == 200
    assert mock_lookup_by_slug.call_count == 1
    assert mock_lookup_by_slug.call_args == mock.call(
        draft_token=None, language_code='en-gb', slug='the-slug'
    )


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_exporting_to_uk_cms_retrieval(mock_lookup_by_slug, client, settings):
    settings.FEATURE_FLAGS['INTERNATIONAL_CONTACT_TRIAGE_ON'] = False
    reload_urlconf()

    mock_lookup_by_slug.return_value = create_response()

    url = reverse(
        'contact-us-exporting-to-the-uk-guidance', kwargs={'slug': 'the-slug'}
    )

    response = client.get(url)

    assert response.status_code == 200
    assert mock_lookup_by_slug.call_count == 1
    assert mock_lookup_by_slug.call_args == mock.call(
        draft_token=None, language_code='en-gb', slug='the-slug'
    )


@pytest.mark.parametrize(
    'url,success_url,view_class,subject,subdomain',
    (
        (
            reverse('contact-us-domestic'),
            reverse('contact-us-domestic-success'),
            views.DomesticFormView,
            settings.CONTACT_DOMESTIC_ZENDESK_SUBJECT,
            None
        ),
        (
            reverse('contact-us-feedback'),
            reverse('contact-us-feedback-success'),
            views.FeedbackFormView,
            settings.CONTACT_DOMESTIC_ZENDESK_SUBJECT,
            None,
        ),
        (
            reverse('contact-us-exporting-to-the-trade-with-uk-app'),
            reverse('contact-us-international-success'),
            views.ExportingToUKFormView,
            settings.CONTACT_INTERNATIONAL_ZENDESK_SUBJECT,
            None,
        ),
        (
            reverse('contact-us-exporting-to-the-uk-import-controls'),
            reverse('contact-us-international-success'),
            views.ExportingToUKFormView,
            settings.CONTACT_INTERNATIONAL_ZENDESK_SUBJECT,
            settings.EU_EXIT_ZENDESK_SUBDOMAIN,
        ),
        (
            reverse('contact-us-exporting-to-the-uk-other'),
            reverse('contact-us-international-success'),
            views.ExportingToUKFormView,
            settings.CONTACT_INTERNATIONAL_ZENDESK_SUBJECT,
            settings.EU_EXIT_ZENDESK_SUBDOMAIN,
        ),
    )
)
@mock.patch.object(views.FormSessionMixin, 'form_session_class')
def test_zendesk_submit_success(
    mock_form_session, client, url, success_url, view_class, subject, settings,
    subdomain
):
    class Form(forms.SerializeDataMixin, django.forms.Form):
        email = django.forms.EmailField()
        save = mock.Mock()
        full_name = 'Foo B'

    with mock.patch.object(view_class, 'form_class', Form):
        response = client.post(url, {'email': 'foo@bar.com'})

    assert response.status_code == 302
    assert response.url == success_url

    assert Form.save.call_count == 1
    assert Form.save.call_args == mock.call(
        email_address='foo@bar.com',
        form_session=mock_form_session(),
        form_url=url,
        full_name='Foo B',
        subject=subject,
        service_name=settings.DIRECTORY_FORMS_API_ZENDESK_SEVICE_NAME,
        sender={'email_address': 'foo@bar.com', 'country_code': None},
        subdomain=subdomain,
    )


def test_contact_us_feedback_prepopulate(client, user):
    url = reverse('contact-us-feedback')
    response = client.get(url)

    assert response.status_code == 200
    assert response.context_data['form'].initial == {
        'email': user.email,
        'name': 'Jim Cross',
    }


@pytest.mark.parametrize('url', (
    reverse('contact-us-enquiries'),
    reverse('contact-us-domestic'),
    reverse('contact-us-dso-form'),
    reverse('contact-us-events-form'),
    reverse('office-finder-contact', kwargs={'postcode': 'FOOBAR'}),
))
def test_contact_us_short_form_prepopualate(client, url, user):
    response = client.get(url)

    assert response.status_code == 200
    assert response.context_data['form'].initial == {
        'email': user.email,
        'company_type': forms.LIMITED,
        'organisation_name': 'Example corp',
        'postcode': 'Foo Bar',
        'family_name': 'Cross',
        'given_name': 'Jim',
    }


def test_contact_us_international_prepopualate(client, user):
    url = reverse('contact-us-international')
    response = client.get(url)

    assert response.status_code == 200
    assert response.context_data['form'].initial == {
        'email': user.email,
        'organisation_name': 'Example corp',
        'country_name': 'FRANCE',
        'city': 'Paris',
        'family_name': 'Cross',
        'given_name': 'Jim'
    }


success_urls = (
    reverse('contact-us-events-success'),
    reverse('contact-us-dso-success'),
    reverse('contact-us-export-advice-success'),
    reverse('contact-us-feedback-success'),
    reverse('contact-us-domestic-success'),
    reverse('contact-us-international-success'),
)


@pytest.mark.parametrize('url', success_urls)
@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@mock.patch.object(views.FormSessionMixin.form_session_class, 'clear')
def test_ingress_url_cleared_on_success(
    mock_clear, mock_lookup_by_slug, url, client, rf
):
    mock_clear.return_value = None
    mock_lookup_by_slug.return_value = create_response()
    # given the ingress url is set
    client.get(
        reverse('contact-us-routing-form', kwargs={'step': 'location'}),
        HTTP_REFERER='http://testserver.com/foo/',
        HTTP_HOST='testserver.com'
    )

    # when the success page is viewed
    response = client.get(url, HTTP_HOST='testserver.com')

    # then the referer is exposed to the template
    assert response.context_data['next_url'] == 'http://testserver.com/foo/'
    assert response.status_code == 200
    # and the ingress url is cleared
    assert mock_clear.call_count == 1


@pytest.mark.parametrize('url', success_urls)
@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@mock.patch.object(views.FormSessionMixin.form_session_class, 'clear')
def test_ingress_url_special_cases_on_success(
    mock_clear, mock_lookup_by_slug, url, client, rf
):
    mock_clear.return_value = None
    mock_lookup_by_slug.return_value = create_response()
    # /contact/<path> should always return to landing
    client.get(
        reverse('contact-us-routing-form', kwargs={'step': 'location'}),
        HTTP_REFERER='http://testserver.com/contact/',
        HTTP_HOST='testserver.com'
    )
    response = client.get(url, HTTP_HOST='testserver.com')
    # for contact ingress urls user flow continues to landing page
    assert response.context_data['next_url'] == '/'
    assert response.status_code == 200
    # and the ingress url is cleared
    assert mock_clear.call_count == 1


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@mock.patch.object(views.FormSessionMixin.form_session_class, 'clear')
def test_always_landing_for_soo_ingress_url_on_success(
    mock_clear, mock_lookup_by_slug, client, rf
):
    mock_clear.return_value = None
    mock_lookup_by_slug.return_value = create_response()
    mocked_soo_landing = 'http://testserver.com/test-path/'
    client.get(
        reverse('contact-us-soo', kwargs={'step': 'organisation'}),
        HTTP_REFERER=mocked_soo_landing + 'markets/details/ebay/',
        HTTP_HOST='testserver.com'
    )
    # when the success page is viewed
    with mock.patch(
        'directory_constants.urls.domestic.SELLING_OVERSEAS',
        mocked_soo_landing
    ):
        response = client.get(
            reverse('contact-us-selling-online-overseas-success'),
            HTTP_HOST='testserver.com'
        )
    # for contact ingress urls user flow continues to landing page
    assert response.context_data['next_url'] == mocked_soo_landing
    assert response.context_data['next_url_text'] == \
        'Go back to Selling Online Overseas'
    assert response.status_code == 200
    # and the ingress url is cleared
    assert mock_clear.call_count == 1


@pytest.mark.parametrize('url', success_urls)
@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@mock.patch.object(views.FormSessionMixin.form_session_class, 'clear')
def test_external_ingress_url_not_used_on_success(
    mock_clear, mock_lookup_by_slug, url, client
):
    mock_clear.return_value = None
    mock_lookup_by_slug.return_value = create_response()
    # given the ingress url is set
    client.get(
        reverse('contact-us-routing-form', kwargs={'step': 'location'}),
        HTTP_REFERER='http://external.com/foo/',
        HTTP_HOST='testserver.com'
    )

    # when the success page is viewed
    response = client.get(url, HTTP_HOST='testserver.com')

    # then the referer is not exposed to the template
    assert response.context_data['next_url'] == '/'
    assert response.status_code == 200


@pytest.mark.parametrize('url', success_urls)
@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@mock.patch.object(views.FormSessionMixin.form_session_class, 'clear')
def test_ingress_url_not_set_on_success(
    mock_clear, mock_lookup_by_slug, url, client
):
    mock_clear.return_value = None
    mock_lookup_by_slug.return_value = create_response()
    # when the success page is viewed and there is no referer set yet
    response = client.get(
        url,
        HTTP_HOST='testserver.com',
        HTTP_REFERER='http://testserver.com/foo/',
    )

    # then the referer is not exposed to the template
    assert response.context_data['next_url'] == '/'
    assert response.status_code == 200


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_internal_ingress_url_used_on_first_step(
    mock_lookup_by_slug, client
):
    mock_lookup_by_slug.return_value = create_response()
    # when an internal ingress url is set
    response = client.get(
        reverse('contact-us-routing-form', kwargs={'step': 'location'}),
        HTTP_REFERER='http://testserver.com/foo/',
        HTTP_HOST='testserver.com'
    )

    # then the referer is exposed to the template
    assert response.context_data['prev_url'] == 'http://testserver.com/foo/'
    assert response.status_code == 200


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_external_ingress_url_not_used_on_first_step(
    mock_lookup_by_slug, client
):
    mock_lookup_by_slug.return_value = create_response()
    # when an external ingress url is set
    response = client.get(
        reverse('contact-us-routing-form', kwargs={'step': 'location'}),
        HTTP_REFERER='http://external.com/foo/',
        HTTP_HOST='testserver.com'
    )

    # then the referer is not exposed to the template
    assert 'prev_url' not in response.context_data
    assert response.status_code == 200


@pytest.mark.parametrize('current_step,choice', (
    (constants.DOMESTIC, constants.TRADE_OFFICE),
    (constants.INTERNATIONAL, constants.INVESTING),
    (constants.INTERNATIONAL, constants.BUYING),
))
@mock.patch.object(views.FormSessionMixin.form_session_class, 'clear')
def test_ingress_url_cleared_on_redirect_away(
    mock_clear, current_step, choice
):
    mock_clear.return_value = None

    form = ChoiceForm(data={'choice': choice})

    view = views.RoutingFormView()
    view.steps = mock.Mock(current=current_step)
    view.storage = mock.Mock()
    view.url_name = 'contact-us-routing-form'

    assert form.is_valid()


def test_selling_online_overseas_contact_form_organisation_url_redirect(client):
    response = client.get(
        reverse('contact-us-soo', kwargs={'step': 'organisation'})
    )
    assert response.status_code == 302
    assert response.url == reverse('contact-us-soo', kwargs={'step': 'contact-details'})


@pytest.mark.parametrize('flow', (
    'CH Company', 'Non-CH Company', 'Individual'
))
@mock.patch('directory_forms_api_client.actions.ZendeskAction')
@mock.patch.object(views.FormSessionMixin, 'form_session_class')
def test_selling_online_overseas_contact_form_submission(
    mock_form_session, mock_zendesk_action, flow, company_profile, user, client
):
    def post(step, args):
        return client.post(
            reverse(url_name, kwargs={'step': step}),
            {
                view_name + '-current_step': step,
                **args
            }
        )

    # Set Directory-API company lookup
    if flow == 'CH Company':
        pass  # lookup defaults to a limited company
    if flow == 'Non-CH Company':
        company_profile.return_value = create_response({
            'company_type': 'SOLE_TRADER',
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
            'summary': 'Makes widgets',
            'website': 'http://www.example.com',
        })
    if flow == 'Individual':
        company_profile.return_value = create_response(status_code=404)

    # Shortcut for company type
    if user.company and 'company_type' in user.company:
        company_type = user.company['company_type']
    else:
        company_type = None

    url_name = 'contact-us-soo'
    view_name = 'selling_online_overseas_form_view'

    # Get the 1st step
    client.get(
        reverse(url_name, kwargs={'step': 'contact-details'}),
        {'market': 'ebay'}
    )

    # Submit the 1st step

    # Note that the user and company fixtures will auto-fill in the details
    # where the form requires it. You can only add optional data
    # to the POST requests.
    response = post('contact-details', {
        'contact-details-phone': '55512345',
        'contact-details-email_pref': True
    })
    assert response.status_code == 302

    if company_type == 'COMPANIES_HOUSE':
        # Name, number and address auto-filled
        response = post('applicant', {
            'applicant-website_address': 'http://fooexample.com',
            'applicant-turnover': 'Under 100k'
        })
    elif company_type == 'SOLE_TRADER':
        # Name, address auto-filled
        response = post('applicant', {
            'applicant-website_address': 'http://fooexample.com',
            'applicant-turnover': 'Under 100k'
        })
    elif company_type is None:
        response = post('applicant', {
            'applicant-company_name': 'Super corp',
            'applicant-company_number': 662222,
            'applicant-company_address': '99 Street',
            'applicant-company_postcode': 'N1 123',
            'applicant-website_address': 'http://barexample.com',
            'applicant-turnover': 'Under 100k'
        })
    assert response.status_code == 302

    response = post('applicant-details', {
        'applicant-details-sku_count': 12,
        'applicant-details-trademarked': True,
    })
    assert response.status_code == 302

    response = post('your-experience', {
        'your-experience-experience': 'Not yet',
        'your-experience-description': 'Makes widgets',
    })
    assert response.status_code == 302
    response = client.get(response.url)
    assert response.status_code == 302

    assert response.url == reverse(
        'contact-us-selling-online-overseas-success'
    )

    # Check data sent to Zendesk
    assert mock_zendesk_action.call_count == 1
    assert mock_zendesk_action.call_args == mock.call(
        subject=settings.CONTACT_SOO_ZENDESK_SUBJECT,
        full_name=user.get_full_name(),
        sender={'email_address': user.email, 'country_code': None},
        email_address=user.email,
        service_name='soo',
        form_url=reverse(
            'contact-us-soo', kwargs={'step': 'contact-details'}
        ),
        form_session=mock_form_session(),
    )
    assert mock_zendesk_action().save.call_count == 1

    expected_data = {
        'market': 'ebay',
        'contact_first_name': 'Jim',
        'contact_last_name': 'Cross',
        'contact_email': 'jim@example.com',
        'phone': '55512345',
        'email_pref': True,
        'sku_count': 12,
        'trademarked': True,
        'experience': 'Not yet',
        'description': 'Makes widgets'
    }
    if company_type == 'COMPANIES_HOUSE':
        expected_data.update({
            'company_name': 'Example corp',
            'company_number': '1234567',
            'company_address': '123 Street, Near Fake Town',
            'website_address': 'http://fooexample.com',
            'turnover': 'Under 100k',
        })
    elif company_type == 'SOLE_TRADER':
        expected_data.update({
            'company_name': 'Example corp',
            'company_address': '123 Street, Near Fake Town',
            'website_address': 'http://fooexample.com',
            'turnover': 'Under 100k',
        })
    elif company_type is None:
        expected_data.update({
            'company_name': 'Super corp',
            'company_number': '662222',
            'company_address': '99 Street',
            'company_postcode': 'N1 123',
            'website_address': 'http://barexample.com',
            'turnover': 'Under 100k',
        })

    cache_key = '{}_{}'.format(view_name, + user.id)
    assert mock_zendesk_action().save.call_args == mock.call(expected_data)
    assert cache.get(cache_key) == expected_data
    # next request for the form will have initial values
    response = client.get(
        reverse(url_name, kwargs={'step': 'contact-details'}),
        {'market': 'ebay'}
    )

    # Initial data contains phone number if company profile present
    if company_type in ['COMPANIES_HOUSE', 'SOLE_TRADER']:
        assert response.context_data['form'].initial == {
            'contact_first_name': 'Jim',
            'contact_last_name': 'Cross',
            'contact_email': 'jim@example.com',
            'phone': '55512345'
        }
    else:
        assert response.context_data['form'].initial == {
            'contact_first_name': 'Jim',
            'contact_last_name': 'Cross',
            'contact_email': 'jim@example.com',
            'phone': '55512345'
        }


def test_selling_online_overseas_contact_form_market_name(client):
    url_name = 'contact-us-soo'

    response = client.get(
        reverse(url_name, kwargs={'step': 'contact-details'}),
        {'market': 'ebay'}
    )
    assert response.status_code == 200
    assert response.context['market_name'] == 'ebay'

    response = client.get(
        reverse(url_name, kwargs={'step': 'applicant'}),
    )
    assert response.status_code == 200
    assert response.context['market_name'] == 'ebay'

    response = client.get(
        reverse(url_name, kwargs={'step': 'applicant-details'}),
    )
    assert response.status_code == 200
    assert response.context['market_name'] == 'ebay'

    response = client.get(
        reverse(url_name, kwargs={'step': 'your-experience'}),
    )
    assert response.status_code == 200
    assert response.context['market_name'] == 'ebay'


@pytest.mark.parametrize('flow', (
    'CH Company', 'Non-CH Company', 'Individual'
))
def test_selling_online_overseas_contact_form_initial_data(flow, company_profile, user, client):

    # Set Directory-API company lookup
    if flow == 'CH Company':
        pass  # lookup defaults to a limited company
    if flow == 'Non-CH Company':
        company_profile.return_value = create_response({
            'company_type': 'SOLE_TRADER',
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
            'summary': 'Makes widgets',
            'website': 'http://www.example.com',
        })
    if flow == 'Individual':
        company_profile.return_value = create_response(status_code=404)

    response = client.get(
        reverse('contact-us-soo', kwargs={'step': 'contact-details'}),
    )
    if flow in ['CH Company', 'Non-CH Company']:
        assert response.context_data['form'].initial == {
            'contact_first_name': 'Jim',
            'contact_last_name': 'Cross',
            'contact_email': 'jim@example.com',
            'phone': '07171771717',
        }
    else:
        assert response.context_data['form'].initial == {
            'contact_first_name': 'Jim',
            'contact_last_name': 'Cross',
            'contact_email': 'jim@example.com'
        }

    response = client.get(
        reverse('contact-us-soo', kwargs={'step': 'applicant'}),
    )
    if flow == 'CH Company':
        assert response.context_data['form'].initial == {
            'company_name': 'Example corp',
            'company_address': '123 Street, Near Fake Town',
            'company_number': 1234567,
            'website_address': 'http://www.example.com',
        }
    if flow == 'Non-CH Company':
        assert response.context_data['form'].initial == {
            'company_name': 'Example corp',
            'company_address': '123 Street, Near Fake Town',
            'website_address': 'http://www.example.com',
        }
    if flow == 'Individual':
        assert response.context_data['form'].initial == {}

    response = client.get(
        reverse('contact-us-soo', kwargs={'step': 'applicant-details'}),
    )
    assert response.context_data['form'].initial == {}

    response = client.get(
        reverse('contact-us-soo', kwargs={'step': 'your-experience'}),
    )
    if flow in ['CH Company', 'Non-CH Company']:
        assert response.context_data['form'].initial == {
            'description': 'Makes widgets'
        }
    else:
        assert response.context_data['form'].initial == {}


def test_office_finder_valid(all_office_details, client):
    with requests_mock.mock() as mock:
        mock.get(url_lookup_by_postcode.format(postcode='ABC123'), json=all_office_details)
        response = client.get(reverse('office-finder'), {'postcode': 'ABC123'})

    assert response.status_code == 200

    assert response.context_data['office_details'] == {
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
    }

    assert response.context_data['other_offices'] == [{
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
    }]


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_contact_us_office_success_next_url(
    mock_lookup_by_slug, client
):
    mock_lookup_by_slug.return_value = create_response()

    url = reverse('contact-us-office-success', kwargs={'postcode': 'FOOBAR'})

    response = client.get(url)

    assert response.status_code == 200
    assert response.context_data['next_url'] == '/'


@pytest.mark.parametrize('url', (
    reverse('contact-us-exporting-to-the-uk'),
    reverse('contact-us-exporting-to-the-uk-defra-success'),
    reverse('contact-us-exporting-to-the-uk-defra'),
    reverse('contact-us-exporting-to-the-uk-beis-success'),
    reverse('contact-us-exporting-to-the-uk-beis'),
    reverse('contact-us-exporting-to-the-uk-guidance', kwargs={'slug': 'foo'})
))
def test_exporting_to_uk_feature_flag_off(url, client, settings):
    settings.FEATURE_FLAGS['EXPORTING_TO_UK_ON'] = False

    response = client.get(url)

    assert response.status_code == 404


@mock.patch.object(views.FormSessionMixin, 'form_session_class')
@mock.patch('contact.forms.ExportVoucherForm.action_class')
def test_export_voucher_submit(mock_gov_notify_action, mock_form_session_class, client, captcha_stub):
    url = reverse('export-voucher-form')
    data = {
        'company_name': 'Example corp',
        'companies_house_number': '012345678',
        'first_name': 'Jim',
        'last_name': 'Example',
        'email': 'jim@example.com',
        'exported_to_eu': True,
        'g-recaptcha-response': captcha_stub,
        'terms_agreed': True,
    }
    response = client.post(url, data=data)

    assert response.status_code == 302
    assert response.url == reverse('export-voucher-success')
    assert mock_gov_notify_action.call_count == 1
    assert mock_gov_notify_action.call_args == mock.call(
        template_id=settings.EXPORT_VOUCHERS_GOV_NOTIFY_TEMPLATE_ID,
        email_address=settings.EXPORT_VOUCHERS_AGENT_EMAIL,
        form_url=reverse('export-voucher-form'),
        form_session=mock_form_session_class(),
        sender=Sender(email_address=data['email'], country_code=None,),
    )
    assert mock_gov_notify_action().save.call_count == 1
    assert mock_gov_notify_action().save.call_args == mock.call({
        'company_name': data['company_name'],
        'companies_house_number': data['companies_house_number'],
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'email': data['email'],
        'exported_to_eu': data['exported_to_eu'],
    })


@pytest.mark.parametrize('enabled', (True, False))
@pytest.mark.parametrize('url', (reverse('export-voucher-success'), reverse('export-voucher-form')))
def test_export_voucher_feature_flag(enabled, url, client, settings):
    settings.FEATURE_FLAGS['EXPORT_VOUCHERS_ON'] = enabled

    response = client.get(url)

    assert response.status_code == 200 if enabled else 404, response.status_code
