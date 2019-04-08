from core.mixins import TranslationsMixin, NotFoundOnDisabledFeature


class HideLanguageSelectorMixin(TranslationsMixin):
    def get_context_data(self, **kwargs):
        return super().get_context_data(
            hide_language_selector=True,
            **kwargs,
        )
