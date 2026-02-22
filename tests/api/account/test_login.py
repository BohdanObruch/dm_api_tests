import pytest
import requests

from src.api.controllers.account.account_controller import AccountApi
from src.api.controllers.account.login_controller import LoginApi
from src.api.models.account.login_model import LoginCredentials, UserEnvelope
from tests.fixtures.allure_helpers import hidden_env, masked_env, step

pytestmark = [pytest.mark.api]


@pytest.mark.smoke
def test_login_success(login_api: LoginApi, user_credentials: dict):
    with step("Mark sensitive login fields as env references"):
        masked_env("LOGIN", "login")
        masked_env("PASSWORD", "password")
    with step("Build login credentials"):
        credentials = LoginCredentials(**user_credentials)
    with step("Login with valid credentials"):
        response = login_api.login(payload=credentials)
    with step("Verify login response"):
        assert isinstance(response, UserEnvelope)
        assert response.resource is not None
        assert response.resource.login == credentials.login


@pytest.mark.regression
def test_login_failure_bad_credentials(login_api: LoginApi, invalid_user_credentials: LoginCredentials):
    with step("Mark sensitive login fields as env references"):
        masked_env("LOGIN", "login")
        masked_env("PASSWORD", "password")
    with step("Login with invalid credentials"), pytest.raises(requests.exceptions.HTTPError) as exc_info:
        login_api.login(payload=invalid_user_credentials)
    with step("Verify status code is 400"):
        assert exc_info.value.response.status_code == 400
    with step("Verify error payload structure"):
        error_response = login_api._response_json(exc_info.value.response)
        assert isinstance(error_response, dict)
        if "message" in error_response:
            assert "User not found or password is incorrect" in error_response["message"]
        elif "invalidProperties" in error_response:
            assert "login" in error_response["invalidProperties"] or "password" in error_response["invalidProperties"]


@pytest.mark.regression
def test_logout(login_api: LoginApi, user_credentials: dict):
    with step("Mark sensitive fields as env references"):
        masked_env("LOGIN", "login")
        masked_env("PASSWORD", "password")
        hidden_env("AUTH_TOKEN", "auth_token")
    with step("Login and retrieve auth token"):
        login_payload = LoginCredentials(**user_credentials)
        login_response = login_api.login(payload=login_payload)
        auth_token = login_response.metadata.get("token")
    with step("Verify auth token is present"):
        assert auth_token is not None
    with step("Logout current session"):
        login_api.logout(x_dm_auth_token=auth_token)
    with step("Verify token is invalidated"):
        account_api = AccountApi(base_url=login_api.base_url, auth_token=auth_token)
        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            account_api.get_current_user()
        assert exc_info.value.response.status_code == 401


@pytest.mark.regression
def test_logout_all(login_api: LoginApi, user_credentials: dict):
    with step("Mark sensitive fields as env references"):
        masked_env("LOGIN", "login")
        masked_env("PASSWORD", "password")
        hidden_env("AUTH_TOKEN", "auth_token")
    with step("Login and retrieve auth token"):
        login_payload = LoginCredentials(**user_credentials)
        login_response = login_api.login(payload=login_payload)
        auth_token = login_response.metadata.get("token")
    with step("Verify auth token is present"):
        assert auth_token is not None
    with step("Logout all sessions"):
        login_api.logout_all(x_dm_auth_token=auth_token)


@pytest.mark.regression
def test_logout_without_token_returns_401(login_api: LoginApi):
    with step("Logout without auth token"), pytest.raises(requests.exceptions.HTTPError) as exc_info:
        login_api._delete("/v1/account/login")
    with step("Verify status code is 401"):
        assert exc_info.value.response.status_code == 401


@pytest.mark.regression
def test_logout_all_without_token_returns_401(login_api: LoginApi):
    with step("Logout all without auth token"), pytest.raises(requests.exceptions.HTTPError) as exc_info:
        login_api._delete("/v1/account/login/all")
    with step("Verify status code is 401"):
        assert exc_info.value.response.status_code == 401
