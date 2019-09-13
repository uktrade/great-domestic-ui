import directory_sso_api_client.models

from django.utils.functional import cached_property

from core import helpers


class SSOUser(directory_sso_api_client.models.SSOUser):

    @cached_property
    def company(self):
        company = helpers.retrieve_company_profile(self.session_id)
        if company:
            return helpers.CompanyParser(company)
