import directory_sso_api_client.models

from django.utils.functional import cached_property

from core import helpers


class SSOUser(directory_sso_api_client.models.SSOUser):

    @cached_property
    def company(self):
        return helpers.company_profile_retrieve(self.session_id)

    @cached_property
    def full_name(self):
        full_name = None
        if self.get_full_name() and self.get_full_name() != '':
            full_name = self.get_full_name()
        elif self.company and 'postal_full_name' in self.company:
            full_name = self.company['postal_full_name']
        return full_name
