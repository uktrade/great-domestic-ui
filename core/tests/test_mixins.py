import pytest

from django.views.generic import TemplateView
from django.utils import translation
from django.http.response import Http404

from core import mixins
from core.tests.helpers import create_response
from sso.models import SSOUser


def test_translate_non_bidi_template(rf):
    class View(mixins.TranslationsMixin, TemplateView):
        template_name_bidi = 'bidi.html'
        template_name = 'non-bidi.html'

    view = View.as_view()
    request = rf.get('/')
    request.LANGUAGE_CODE = 'en-gb'

    response = view(request)

    assert response.status_code == 200
    assert response.template_name == ['non-bidi.html']


def test_get_cms_component_mixin_is_bidi_no_cms_component(rf):
    class View(mixins.GetCMSComponentMixin, TemplateView):
        template_name = 'thing.html'
        cms_component = None

    view = View.as_view()
    request = rf.get('/')
    response = view(request)

    assert response.context_data['component_is_bidi'] is False
    assert response.context_data['cms_component'] is None


@pytest.mark.parametrize('activated_language,component_langages,expected', [
    ('en-gb', [['ar', 'Arabic']], False),
    ('en-gb', [['en-gb', 'English']], False),
    ('en-gb', [['ar', 'Arabic'], ['en-gb', 'English']], False),
    ('ar', [['ar', 'Arabic']], True),
    ('ar', [['en-gb', 'English']], False),
    ('ar', [['ar', 'Arabic'], ['en-gb', 'English']], True),
])
def test_get_cms_component_mixin_is_bidi_cms_component_not_bidi(
    rf, activated_language, component_langages, expected
):
    class View(mixins.GetCMSComponentMixin, TemplateView):
        template_name = 'thing.html'
        cms_component = {
            'meta': {
                'languages': component_langages
            }
        }

    view = View.as_view()
    request = rf.get('/')
    with translation.override(activated_language):
        response = view(request)

    assert response.context_data['component_is_bidi'] is expected
    assert response.context_data['cms_component'] == View.cms_component


@pytest.mark.parametrize('full_name,first_name,last_name', (
    ('James Example', 'James', 'Example'),
    ('James', 'James', None),
    ('James Earl Jones', 'James', 'Jones'),
    ('', None, None),
))
def test_retrieve_company_profile_mixin_name_guessing(rf, full_name, first_name, last_name, company_profile):
    company_profile.return_value = create_response({'postal_full_name': full_name})
    request = rf.get('/')
    request.user = SSOUser(session_id=123)
    mixin = mixins.PrepopulateFormMixin()
    mixin.request = request

    assert mixin.guess_given_name == first_name
    assert mixin.guess_family_name == last_name


@pytest.mark.parametrize('full_name,first_name,last_name', (
    ('James Example', 'James', 'Example'),
    ('James', 'James', None),
    ('James Earl Jones', 'James', 'Jones'),
    ('', None, None),
))
def test_retrieve_company_profile_mixin_name_guessing_user(rf, full_name, first_name, last_name, company_profile):
    company_profile.return_value = create_response(status_code=404)
    request = rf.get('/')
    request.user = SSOUser(session_id=123, first_name=first_name, last_name=last_name)
    mixin = mixins.PrepopulateFormMixin()
    mixin.request = request

    assert mixin.guess_given_name == first_name
    assert mixin.guess_family_name == last_name


def test_prototype_feature_flag_mixin_on(rf, settings):
    class TestView(mixins.PrototypeFeatureFlagMixin, TemplateView):
        template_name = 'core/base.html'

    settings.FEATURE_FLAGS['PROTOTYPE_PAGES_ON'] = True

    request = rf.get('/')

    response = TestView.as_view()(request)

    assert response.status_code == 200


def test_prototype_feature_flag_mixin_off(rf, settings):
    class TestView(mixins.PrototypeFeatureFlagMixin, TemplateView):
        template_name = 'core/base.html'

    settings.FEATURE_FLAGS['PROTOTYPE_PAGES_ON'] = False

    request = rf.get('/')
    with pytest.raises(Http404):
        TestView.as_view()(request)
