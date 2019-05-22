from directory_constants.choices import COUNTRY_CHOICES

from ukef import forms


def test_contact_form_validations(valid_contact_form_data):
    form = forms.UKEFContactForm(data=valid_contact_form_data)
    assert form.is_valid()
    assert form.cleaned_data['full_name'] == valid_contact_form_data[
        'full_name'
    ]
    assert form.cleaned_data['email'] == valid_contact_form_data['email']


def test_contact_form_api_serialization(valid_contact_form_data):
    form = forms.UKEFContactForm(data=valid_contact_form_data)
    assert form.is_valid()

    api_data = form.serialized_data
    country_label = dict(COUNTRY_CHOICES).get(
        form.cleaned_data['country']
    )
    assert api_data['country_label'] == country_label


def test_community_form_api_serialization_with_other_options(
    valid_contact_form_data_with_extra_options
):
    form = forms.UKEFContactForm(
        data=valid_contact_form_data_with_extra_options
    )
    assert form.is_valid()
    assert form.cleaned_data['like_to_discuss'] == 'yes'
    api_data = form.serialized_data
    like_to_discuss_country = dict(COUNTRY_CHOICES).get(
        form.cleaned_data['like_to_discuss_other']
    )
    assert api_data['like_to_discuss_country'] == like_to_discuss_country
