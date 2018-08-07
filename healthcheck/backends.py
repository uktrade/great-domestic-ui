from directory_api_client.client import api_client
from directory_sso_api_client.client import sso_api_client
from health_check.backends import BaseHealthCheckBackend
from health_check.exceptions import (
    ServiceReturnedUnexpectedResult, ServiceUnavailable
)


class APIProxyBackend(BaseHealthCheckBackend):

    message_bad_status = 'api proxy returned {0.status_code} status code'

    def check_status(self):
        try:
            response = api_client.ping()
        except Exception as error:
            raise ServiceUnavailable('(API proxy) ' + str(error))
        else:
            if response.status_code != 200:
                raise ServiceReturnedUnexpectedResult(
                    self.message_bad_status.format(response)
                )
        return True


class SingleSignOnBackend(BaseHealthCheckBackend):

    message_bad_status = 'SSO proxy returned {0.status_code} status code'

    def check_status(self):
        try:
            response = sso_api_client.ping()
        except Exception as error:
            raise ServiceUnavailable('(SSO proxy) ' + str(error))
        else:
            if response.status_code != 200:
                raise ServiceReturnedUnexpectedResult(
                    self.message_bad_status.format(response)
                )
        return True
