from django.conf import settings

from core.mixins import NotFoundOnDisabledFeature


class TestSearchAPIFeatureFlagMixin(NotFoundOnDisabledFeature):
    @property
    def flag(self):
        return settings.FEATURE_FLAGS['TEST_SEARCH_API_PAGES_ON']