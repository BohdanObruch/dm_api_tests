from __future__ import annotations

import pytest
import requests

from src.api.controllers.account.account_controller import AccountApi
from src.api.models.account.account_model import UserEnvelope
from src.api.models.account.login_model import LoginCredentials
from tests.fixtures.allure_helpers import hidden_env, masked_env, step


@pytest.mark.smoke
def test_register_success(account_api: AccountApi, random_user_credentials: dict[str, str]):
    with step("Mark registration credentials as env references"):
        masked_env("LOGIN", "login")
        masked_env("EMAIL", "email")
        masked_env("PASSWORD", "password")
    with step("Register user"):
        registered = account_api.register(random_user_credentials)
    with step("Verify registration response"):
        assert isinstance(registered, UserEnvelope)


@pytest.mark.regression
def test_register_duplicate_returns_400(account_api: AccountApi, random_user_credentials: dict[str, str]):
    with step("Mark registration credentials as env references"):
        masked_env("LOGIN", "login")
        masked_env("EMAIL", "email")
        masked_env("PASSWORD", "password")
    with step("Register user first time"):
        account_api.register(random_user_credentials)
    with step("Register duplicate user and verify 400"):
        with pytest.raises(requests.HTTPError) as exc_info:
            account_api.register(random_user_credentials)
        assert exc_info.value.response.status_code == 400


@pytest.mark.regression
def test_register_invalid_payload_returns_400(account_api: AccountApi):
    with step("Register user with invalid payload"), pytest.raises(requests.HTTPError) as exc_info:
        account_api.register({"login": "", "email": "bad-email"})
    with step("Verify status code is 400"):
        assert exc_info.value.response.status_code == 400


@pytest.mark.smoke
def test_get_current_user_success(authed_account_api: AccountApi, user_login: str):
    with step("Mark login value as env reference"):
        masked_env("LOGIN", "user_login")
    with step("Get current user"):
        current = authed_account_api.get_current_user()
    with step("Verify current user login"):
        assert current.resource is not None
        assert current.resource.login == user_login


@pytest.mark.regression
def test_get_current_user_without_token_returns_auth_error(configs):
    with step("Create unauthenticated account api"):
        unauthenticated_api = AccountApi(base_url=configs.base_url)
    with step("Get current user without token"), pytest.raises(requests.HTTPError) as exc_info:
        unauthenticated_api.get_current_user()
    with step("Verify status code is 401 or 403"):
        assert exc_info.value.response.status_code in (401, 403)


@pytest.mark.regression
def test_activate_invalid_token_returns_400_or_410(account_api: AccountApi):
    with step("Activate account with invalid token"), pytest.raises(requests.HTTPError) as exc_info:
        account_api.activate(token="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 400 or 410"):
        assert exc_info.value.response.status_code in (400, 410)


@pytest.mark.regression
def test_reset_password_success(account_api: AccountApi, fresh_session_user):
    with step("Mark reset fields as env references"):
        masked_env("LOGIN", "login")
        masked_env("EMAIL", "email")
    with step("Reset password for existing user"):
        reset_result = account_api.reset_password(
            {"login": fresh_session_user.login, "email": fresh_session_user.email}
        )
    with step("Verify reset response exists"):
        assert reset_result is not None


@pytest.mark.regression
def test_reset_password_invalid_payload_returns_400(account_api: AccountApi):
    with step("Reset password with invalid payload"), pytest.raises(requests.HTTPError) as exc_info:
        account_api.reset_password({"login": "unknown_user"})
    with step("Verify status code is 400"):
        assert exc_info.value.response.status_code == 400


@pytest.mark.regression
def test_change_password_success_and_revert(
    authed_account_api: AccountApi,
    login_api,
    user_login: str,
    user_password: str,
):
    with step("Mark sensitive fields as env references"):
        masked_env("LOGIN", "login")
        masked_env("PASSWORD", "old_password")
        masked_env("PASSWORD", "new_password")
        hidden_env("AUTH_TOKEN", "auth_token")
    with step("Prepare new password"):
        new_password = "Aa1!" + user_password[::-1]
    with step("Change password"):
        changed = authed_account_api.change_password(
            {
                "login": user_login,
                "oldPassword": user_password,
                "newPassword": new_password,
            }
        )
    with step("Verify change password response"):
        assert isinstance(changed, UserEnvelope)
    with step("Login with new password"):
        login_result = login_api.login(
            payload=LoginCredentials(login=user_login, password=new_password, remember_me=True)
        )
    with step("Verify login with new password"):
        assert login_result.resource is not None
        assert login_result.resource.login == user_login
    with step("Revert password to original value"):
        new_token = (login_result.metadata or {}).get("token")
        reverter_api = (
            authed_account_api
            if not isinstance(new_token, str)
            else AccountApi(base_url=authed_account_api.base_url, auth_token=new_token)
        )
        reverter_api.change_password(
            {
                "login": user_login,
                "oldPassword": new_password,
                "newPassword": user_password,
            }
        )


@pytest.mark.regression
def test_change_password_invalid_payload_returns_400(authed_account_api: AccountApi, user_login: str):
    with step("Mark login as env reference"):
        masked_env("LOGIN", "login")
    with step("Change password with invalid payload"), pytest.raises(requests.HTTPError) as exc_info:
        authed_account_api.change_password({"login": user_login, "oldPassword": "x"})
    with step("Verify status code is 400"):
        assert exc_info.value.response.status_code == 400


@pytest.mark.regression
def test_change_email_success(authed_account_api: AccountApi, user_login: str, user_password: str):
    with step("Mark sensitive fields as env references"):
        masked_env("LOGIN", "login")
        masked_env("PASSWORD", "password")
        masked_env("EMAIL", "email")
    with step("Change account email"):
        changed = authed_account_api.change_email(
            {
                "login": user_login,
                "password": user_password,
                "email": f"new_{user_login}@example.com",
            }
        )
    with step("Verify change email response"):
        assert isinstance(changed, UserEnvelope)


@pytest.mark.regression
def test_change_email_invalid_payload_returns_400(authed_account_api: AccountApi, user_login: str, user_password: str):
    with step("Mark sensitive fields as env references"):
        masked_env("LOGIN", "login")
        masked_env("PASSWORD", "password")
    with step("Change email with invalid payload"), pytest.raises(requests.HTTPError) as exc_info:
        authed_account_api.change_email({"login": user_login, "password": user_password})
    with step("Verify status code is 400"):
        assert exc_info.value.response.status_code == 400
