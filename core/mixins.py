from django.http import Http404
from django.conf import settings
from django.utils import translation
from django.utils.functional import cached_property

from directory_cms_client.client import cms_api_client
from directory_cms_client.helpers import (
    handle_cms_response, handle_cms_response_allow_404
)
from directory_constants import cms
from directory_components.mixins import GA360Mixin

from . import helpers


class NotFoundOnDisabledFeature:
    def dispatch(self, *args, **kwargs):
        if not self.flag:
            raise Http404()
        return super().dispatch(*args, **kwargs)


class CampaignPagesFeatureFlagMixin(NotFoundOnDisabledFeature):
    @property
    def flag(self):
        return settings.FEATURE_FLAGS['CAMPAIGN_PAGES_ON']


class NewsSectionFeatureFlagMixin(NotFoundOnDisabledFeature):
    @property
    def flag(self):
        return settings.FEATURE_FLAGS['NEWS_SECTION_ON']


class PrototypeFeatureFlagMixin(NotFoundOnDisabledFeature):
    @property
    def flag(self):
        return settings.FEATURE_FLAGS['PROTOTYPE_PAGES_ON']


class MarketAccessFeatureFlagMixin(NotFoundOnDisabledFeature):
    @property
    def flag(self):
        return settings.FEATURE_FLAGS['MARKET_ACCESS_ON']


class GetCMSPageMixin:

    @cached_property
    def page(self):
        response = cms_api_client.lookup_by_slug(
            slug=self.slug,
            language_code=translation.get_language(),
            draft_token=self.request.GET.get('draft_token'),
        )
        return handle_cms_response(response)

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(page=self.page, *args, **kwargs)


class GetCMSComponentMixin:
    @cached_property
    def cms_component(self):
        response = cms_api_client.lookup_by_slug(
            slug=self.component_slug,
            language_code=translation.get_language(),
            service_name=cms.COMPONENTS,
        )
        return handle_cms_response_allow_404(response)

    @property
    def component_is_bidi(self):
        if self.cms_component:
            return helpers.cms_component_is_bidi(
                translation.get_language(),
                self.cms_component['meta']['languages']
            )
        return False

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            component_is_bidi=self.component_is_bidi,
            cms_component=self.cms_component,
            *args, **kwargs
        )


class TranslationsMixin:

    def dispatch(self, request, *args, **kwargs):
        translation.activate(request.LANGUAGE_CODE)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['LANGUAGE_BIDI'] = translation.get_language_bidi()
        context['directory_components_html_lang_attribute']\
            = translation.get_language()
        return context


class PreventCaptchaRevalidationMixin:
    """When get_all_cleaned_data() is called the forms are revalidated,
    which causes captcha to fail becuase the same captcha response from google
    is posted to google multiple times. This captcha response is a nonce, and
    so google complains the second time it's seen.

    This is worked around by removing captcha from the form before the view
    calls get_all_cleaned_data

    """

    should_ignore_captcha = False

    def render_done(self, *args, **kwargs):
        self.should_ignore_captcha = True
        return super().render_done(*args, **kwargs)

    def get_form(self, step=None, *args, **kwargs):
        form = super().get_form(step=step, *args, **kwargs)
        if step == self.steps.last and self.should_ignore_captcha:
            del form.fields['captcha']
        return form


class PrepopulateFormMixin:

    @cached_property
    def company_profile(self):
        return helpers.get_company_profile(self.request)

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['initial'] = self.get_form_initial()
        return form_kwargs

    @property
    def guess_given_name(self):
        if self.company_profile and self.company_profile['postal_full_name']:
            name = self.company_profile['postal_full_name']
            return name.split(' ')[0]

    @property
    def guess_family_name(self):
        if self.company_profile and self.company_profile['postal_full_name']:
            names = self.company_profile['postal_full_name'].split(' ')
            return names[-1] if len(names) > 1 else None


class SetGA360ValuesForCMSPageMixin(GA360Mixin):
    """
    Expects the view to have the `page` attribute and uses the
    page's `tree_based_breadcrumbs` to work out page section.
    """

    def dispatch(self, request, *args, **kwargs):
        dispatch_result = super().dispatch(request, *args, **kwargs)

        page_id = self.page['page_type']

        breadcrumbs = self.page['tree_based_breadcrumbs']
        site_subsection = self.page['title']
        site_section = ''

        # get the page one level up from the current page
        if len(breadcrumbs) > 1:
            site_section = breadcrumbs[-2]['title']

        self.set_ga360_payload(
            page_id=page_id,
            business_unit=settings.GA360_BUSINESS_UNIT,
            site_section=site_section,
            site_subsection=site_subsection
        )

        return dispatch_result


class SetGA360ValuesMixin(GA360Mixin):
    """
    Variation of the above mixin for non-CMS pages. Uses the view's `page_type`
    attribute to map to values in core.helpers.GA_DATA_MAPPING.
    """

    def dispatch(self, request, *args, **kwargs):
        dispatch_result = super().dispatch(request, *args, **kwargs)

        page_type = self.page_type
        ga360_data = helpers.get_ga_data_for_page(page_type)

        self.set_ga360_payload(
            page_id=page_type,
            business_unit=settings.GA360_BUSINESS_UNIT,
            site_section=ga360_data['site_section'],
            site_subsection=ga360_data['site_subsection']
        )
        return dispatch_result
