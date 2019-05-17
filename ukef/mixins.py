from django.conf import settings

from core.mixins import NotFoundOnDisabledFeature


class UKEFPagesFeatureFlagMixin(NotFoundOnDisabledFeature):

    @property
    def flag(self):
        return settings.FEATURE_FLAGS['UKEF_PAGES_ON']
