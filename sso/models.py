import directory_sso_api_client.models

from django.utils.functional import cached_property

from core import helpers


class SSOUser(directory_sso_api_client.models.SSOUser):

    @cached_property
    def company(self):
        return helpers.company_profile_retrieve(self.session_id)

    def get_full_name(self):
        full_name = super().get_full_name()
        if not full_name and self.company:
            full_name = self.company['postal_full_name']
        return full_name
