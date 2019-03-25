from collections import OrderedDict

from django.shortcuts import redirect
from formtools.wizard.views import NamedUrlWizardView

from sso.utils import SSOLoginRequiredMixin


class NamedUrlCacheWizardView(NamedUrlWizardView):
    storage_name = 'core.wizard.storage.CacheStorage'


class CacheLastUserSubmissionWizardView(
    SSOLoginRequiredMixin, NamedUrlCacheWizardView
):
    def get_prefix(self, request, *args, **kwargs):
        return '{}_{}'.format(
            super().get_prefix(request, *args, **kwargs), request.sso_user.id)

    def render_done(self, form, **kwargs):
        # copied from NamedUrlWizardView
        if kwargs.get('step', None) != self.done_step_name:
            return redirect(self.get_step_url(self.done_step_name))

        # copied from WizardView
        final_forms = OrderedDict()
        for form_key in self.get_form_list():
            form_obj = self.get_form(
                step=form_key,
                data=self.storage.get_step_data(form_key),
                files=self.storage.get_step_files(form_key)
            )
            if not form_obj.is_valid():
                return self.render_revalidation_failure(
                    form_key, form_obj, **kwargs)
            final_forms[form_key] = form_obj
        done_response = self.done(
            final_forms.values(), form_dict=final_forms, **kwargs)

        # EDITED: don't reset storage after successfull submission
        # self.storage.reset()

        return done_response
