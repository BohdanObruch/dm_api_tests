from __future__ import annotations

import pytest
from faker import Faker

from src.api.controllers.account.account_controller import AccountApi
from src.api.models.account.login_model import LoginCredentials
from tests.fixtures.api import SessionUser
from tests.fixtures.config import Config

fake = Faker()


@pytest.fixture(scope="function")
def authed_account_api(configs: Config, auth_token: str) -> AccountApi:
    return AccountApi(base_url=configs.base_url, auth_token=auth_token)


@pytest.fixture(scope="function")
def random_user_credentials() -> dict[str, str]:
    login = f"acc_{fake.user_name()}_{fake.pyint(min_value=1000, max_value=9999)}"
    return {
        "login": login,
        "email": f"{login}@example.com",
        "password": fake.password(length=14),
    }


@pytest.fixture(scope="function")
def user_credentials(fresh_session_user: SessionUser) -> dict[str, str]:
    return {
        "login": fresh_session_user.login,
        "password": fresh_session_user.password,
        "rememberMe": True,
    }


@pytest.fixture(scope="session")
def invalid_user_credentials() -> LoginCredentials:
    return LoginCredentials(login="nonexistent_user", password="wrong_password", rememberMe=False)
