from directory_constants import choices
import pytest

from euexit import forms


@pytest.fixture
def domestic_contact_form_data(captcha_stub):
    return {
        'first_name': 'test',
        'last_name': 'example',
        'email': 'test@example.com',
        'organisation_type': 'COMPANY',
        'company_name': 'thing',
        'comment': 'hello',
        'terms_agreed': True,
        'g-recaptcha-response': captcha_stub,
    }


@pytest.fixture
def international_contact_form_data(captcha_stub):
    return {
        'first_name': 'test',
        'last_name': 'example',
        'email': 'test@example.com',
        'organisation_type': 'COMPANY',
        'company_name': 'thing',
        'country': choices.COUNTRY_CHOICES[1][0],
        'city': 'London',
        'comment': 'hello',
        'terms_agreed': True,
        'g-recaptcha-response': captcha_stub,
    }


@pytest.mark.parametrize('form_class', (
    forms.InternationalContactForm, forms.DomesticContactForm
))
def test_contact_form_set_field_attributes(form_class):
    form_one = form_class(
        field_attributes={},
        ingress_url='http://www.ingress.com',
        disclaimer='disclaim',
    )
    form_two = form_class(
        field_attributes={
            'first_name': {
                'label': 'Your given name',
            },
            'last_name': {
                'label': 'Your family name'
            }
        },
        ingress_url='http://www.ingress.com',
        disclaimer='disclaim',
    )

    assert form_one.fields['first_name'].label is None
    assert form_one.fields['last_name'].label is None
    assert form_one.fields['terms_agreed'].widget.label.endswith('disclaim')
    assert form_two.fields['first_name'].label == 'Your given name'
    assert form_two.fields['last_name'].label == 'Your family name'
    assert form_two.fields['terms_agreed'].widget.label.endswith('disclaim')


def test_domestic_contact_form_serialize(captcha_stub):
    form = forms.DomesticContactForm(
        field_attributes={},
        ingress_url='http://www.ingress.com',
        disclaimer='disclaim',
        data={
            'first_name': 'test',
            'last_name': 'example',
            'email': 'test@example.com',
            'organisation_type': 'COMPANY',
            'company_name': 'thing',
            'comment': 'hello',
            'terms_agreed': True,
            'g-recaptcha-response': captcha_stub,
        }
    )
    assert form.is_valid()
    assert form.serialized_data == {
        'first_name': 'test',
        'last_name': 'example',
        'email': 'test@example.com',
        'organisation_type': 'COMPANY',
        'company_name': 'thing',
        'comment': 'hello',
        'ingress_url': 'http://www.ingress.com',
    }


def test_international_contact_form_serialize(captcha_stub):
    form = forms.InternationalContactForm(
        field_attributes={},
        ingress_url='http://www.ingress.com',
        disclaimer='disclaim',
        data={
            'first_name': 'test',
            'last_name': 'example',
            'email': 'test@example.com',
            'organisation_type': 'COMPANY',
            'company_name': 'thing',
            'country': choices.COUNTRY_CHOICES[1][0],
            'city': 'London',
            'comment': 'hello',
            'terms_agreed': True,
            'g-recaptcha-response': captcha_stub,
        }
    )

    assert form.is_valid()
    assert form.serialized_data == {
        'first_name': 'test',
        'last_name': 'example',
        'email': 'test@example.com',
        'organisation_type': 'COMPANY',
        'company_name': 'thing',
        'country': choices.COUNTRY_CHOICES[1][0],
        'city': 'London',
        'comment': 'hello',
        'ingress_url': 'http://www.ingress.com',
    }
