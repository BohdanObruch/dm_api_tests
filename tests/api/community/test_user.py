import pytest
import requests

from src.api.controllers.community.user_controller import UserApi
from src.api.models.community.user_model import UserDetailsEnvelope, UserEnvelope, UserListEnvelope
from tests.fixtures.allure_helpers import step

pytestmark = [pytest.mark.api]


@pytest.mark.smoke
def test_get_users_list(user_api):
    with step("Get users list"):
        response = user_api.list()
    with step("Verify users list response"):
        assert isinstance(response, UserListEnvelope)
        assert response.resources is None or isinstance(response.resources, list)


@pytest.mark.regression
def test_get_user_by_login(user_api, community_user_login: str):
    with step("Get user by login"):
        response = user_api.get_by_login(login=community_user_login)
    with step("Verify user envelope and login"):
        assert isinstance(response, UserEnvelope)
        assert response.resource is not None
        assert response.resource.login == community_user_login


@pytest.mark.regression
def test_get_user_details_by_login(user_api, community_user_login: str):
    with step("Get user details by login"):
        response = user_api.get_details_by_login(login=community_user_login)
    with step("Verify user details envelope and login"):
        assert isinstance(response, UserDetailsEnvelope)
        assert response.resource is not None
        assert response.resource.login == community_user_login


@pytest.mark.regression
def test_update_user_details_roundtrip(user_api, community_user_login: str):
    with step("Get original user details"):
        original = user_api.get_details_by_login(login=community_user_login)
    with step("Verify original details are present"):
        assert original.resource is not None
    with step("Prepare update payload from original values"):
        payload = {
            "name": original.resource.name or "Auto Test User",
            "location": original.resource.location or "Test Location",
            "status": original.resource.status or "Ready",
        }
    with step("Update user details"):
        updated = user_api.update_details_by_login(login=community_user_login, payload=payload)
    with step("Verify updated user details"):
        assert isinstance(updated, UserDetailsEnvelope)
        assert updated.resource is not None
        assert updated.resource.login == community_user_login


@pytest.mark.regression
def test_update_user_details_without_token_returns_401(configs, community_user_login: str):
    with step("Create unauthenticated user api"):
        unauth_api = UserApi(base_url=configs.app_base_url)
    with step("Try to update user details without token"), pytest.raises(requests.HTTPError) as exc_info:
        unauth_api.update_details_by_login(login=community_user_login, payload={"status": "unauth-test"})
    with step("Verify status code is 401"):
        assert exc_info.value.response.status_code == 401
