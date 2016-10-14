import http
from unittest import mock

from django.core.urlresolvers import reverse

from registration.clients.directory_api import api_client
from user.views import UserProfileDetailView


@mock.patch.object(api_client.user, 'retrieve_profile')
def test_user_profile_details_calls_api(mock_retrieve_profile, rf):
    view = UserProfileDetailView.as_view()
    request = rf.get(reverse('user-detail'))
    view(request)
    # TODO: ED-183
    # update test once no longer hard-coding the user id
    assert mock_retrieve_profile.called_once()


@mock.patch.object(api_client.user, 'retrieve_profile')
def test_user_profile_details_exposes_context(mock_retrieve_profile, rf):
    mock_retrieve_profile.return_value = expected_context = {
        'email': 'jim@example.com',
        'name': 'Jim Jackson',
    }
    view = UserProfileDetailView.as_view()
    request = rf.get(reverse('user-detail'))
    response = view(request)
    assert response.status_code == http.client.OK
    assert response.template_name == [UserProfileDetailView.template_name]
    assert response.context_data['user'] == expected_context
