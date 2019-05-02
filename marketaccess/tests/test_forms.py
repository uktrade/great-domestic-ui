import pytest

from marketaccess import forms


@pytest.fixture
def about_form_data():
    return {
        'firstname': 'Craig',
        'lastname': 'Smith',
        'jobtitle': 'Musician',
        'business_type': "I’m an exporter or investor, or \
                          I want to export or invest",
        'other_business_type': '',
        'company_name': 'Craig Music',
        'email': 'craig@craigmusic.com',
        'phone': '0123456789'
    }


@pytest.fixture
def about_form_data_with_other_business_type():
    return {
        'firstname': 'Craig',
        'lastname': 'Smith',
        'jobtitle': 'Musician',
        'business_type': "Other",
        'other_business_type': "Other business type",
        'company_name': 'Craig Music',
        'email': 'craig@craigmusic.com',
        'phone': '0123456789'
    }


def test_about_form_initial():
    form = forms.AboutForm()
    assert form.fields['firstname'].initial is None
    assert form.fields['lastname'].initial is None
    assert form.fields['jobtitle'].initial is None
    assert form.fields['business_type'].initial is None
    assert form.fields['other_business_type'].initial is None
    assert form.fields['company_name'].initial is None
    assert form.fields['email'].initial is None
    assert form.fields['phone'].initial is None


def test_about_form_mandatory_fields():
    form = forms.AboutForm(data={})

    assert form.fields['firstname'].required is True
    assert form.fields['lastname'].required is True
    assert form.fields['jobtitle'].required is True
    assert form.fields['business_type'].required is True
    assert form.fields['other_business_type'].required is False
    assert form.fields['company_name'].required is True
    assert form.fields['email'].required is True
    assert form.fields['phone'].required is True


def test_about_form_serialize():
    form = forms.AboutForm(
        data=about_form_data()
    )
    assert form.is_valid()
    assert form.cleaned_data == about_form_data()


def test_about_form_with_other_serializes():
    form = forms.AboutForm(
        data=about_form_data_with_other_business_type()
    )

    assert form.is_valid()
    assert form.cleaned_data == about_form_data_with_other_business_type()


def test_other_business_type_is_required_if_other_business_type():
    form_data = about_form_data_with_other_business_type()
    form_data['other_business_type'] = ''
    form = forms.AboutForm(
        data=form_data
    )

    assert len(form.errors) == 1
    assert form.errors['other_business_type'] == [
        'Enter your organisation'
    ]


def test_about_form_error_messages():
    form = forms.AboutForm(
        data={}
    )

    assert len(form.errors) == 7
    form.errors['firstname'] == ['Enter your first name']
    form.errors['lastname'] == ['Enter your last name']
    form.errors['jobtitle'] == ['Enter your job title']
    form.errors['business_type'] == ['Enter your business type']
    form.errors['company_name'] == ['Enter your company name']
    form.errors['email'] == ['Enter your email']
    form.errors['phone'] == ['Enter your phone number']


@pytest.fixture
def problem_details_form_data():
    return {
        'product_service': 'something',
        'location': 'Angola',
        'problem_summary': 'problem summary',
        'impact': 'problem impact',
        'resolve_summary': 'steps in resolving',
        'eu_exit_related': 'No',
    }


def test_problem_details_form_initial():
    form = forms.ProblemDetailsForm()
    assert form.fields['product_service'].initial is None
    assert form.fields['location'].initial is None
    assert form.fields['problem_summary'].initial is None
    assert form.fields['impact'].initial is None
    assert form.fields['resolve_summary'].initial is None
    assert form.fields['eu_exit_related'].initial is None


def test_problem_details_form_mandatory_fields():
    form = forms.ProblemDetailsForm(data={})

    assert form.fields['product_service'].required is True
    assert form.fields['location'].required is True
    assert form.fields['problem_summary'].required is True
    assert form.fields['impact'].required is True
    assert form.fields['resolve_summary'].required is True
    assert form.fields['eu_exit_related'].required is True


def test_problem_details_form_serialize():
    form = forms.ProblemDetailsForm(
        data=problem_details_form_data()
    )
    assert form.is_valid()
    assert form.cleaned_data == problem_details_form_data()


def test_problem_details_error_messages():
    form = forms.ProblemDetailsForm(
        data={}
    )

    assert len(form.errors) == 6
    form.errors['product_service'] == [
        'Tell us what you’re trying to export or invest in'
    ]
    form.errors['location'] == [
        'Tell us where are you trying to export to or invest in'
        ]
    form.errors['problem_summary'] == [
        'Tell us about the problem you’re facing'
    ]
    form.errors['impact'] == [
        'Tell us how your business is being affected by the problem'
    ]
    form.errors['resolve_summary'] == [
        'Tell us what you’ve done to resolve your problem, \
        even if this is your first step'
    ]
    form.errors['eu_exit_related'] == [
        'Tell us if your problem is related to EU Exit'
    ]


@pytest.fixture
def other_details_form_data():
    return {
        'other_details': 'additional details'
    }


def test_other_details_form_initial():
    form = forms.OtherDetailsForm()
    assert form.fields['other_details'].initial is None


def test_other_details_form_mandatory_fields():
    form = forms.OtherDetailsForm(data={})

    assert form.fields['other_details'].required is False


def test_other_details_form_serialize():
    form = forms.OtherDetailsForm(
        data=other_details_form_data()
    )
    assert form.is_valid()
    assert form.cleaned_data == other_details_form_data()
