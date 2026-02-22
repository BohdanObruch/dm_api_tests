from __future__ import annotations

import re
import time
from dataclasses import dataclass

import pytest
import requests
from faker import Faker

from src.api.controllers.account.account_controller import AccountApi
from src.api.controllers.account.login_controller import LoginApi
from src.api.models.account.login_model import LoginCredentials
from tests.fixtures.config import Config

fake = Faker()
UUID_RE = re.compile(
    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
)


@dataclass(frozen=True)
class SessionUser:
    login: str
    password: str
    email: str
    token: str


def extract_activation_token_from_mailhog(mail_hog_url: str, email: str, timeout_sec: int = 60) -> str | None:
    mailbox, _, domain = email.partition("@")
    if not mailbox or not domain:
        return None

    deadline = time.time() + timeout_sec
    endpoint = f"{mail_hog_url.rstrip('/')}/api/v2/messages"
    while time.time() < deadline:
        try:
            response = requests.get(endpoint, timeout=15)
            response.raise_for_status()
            items = response.json().get("items", [])
        except Exception:
            time.sleep(2)
            continue

        for message in items:
            recipients = message.get("To", [])
            is_for_user = any(
                recipient.get("Mailbox") == mailbox and recipient.get("Domain") == domain
                for recipient in recipients
            )
            if not is_for_user:
                continue

            body = (message.get("Content", {}) or {}).get("Body", "")
            match = UUID_RE.search(body)
            if match:
                return match.group(0)

        time.sleep(2)

    return None


def _create_active_session_user(configs: Config, login_api: LoginApi, account_api: AccountApi, prefix: str) -> SessionUser:
    login = f"{prefix}_{fake.user_name()}_{fake.pyint(min_value=1000, max_value=9999)}"
    password = fake.password(length=14)
    email = f"{login}@example.com"

    try:
        account_api.register(payload={"login": login, "email": email, "password": password})
    except requests.HTTPError as exc:
        pytest.fail(f"Could not register user {login}: {exc}")

    activation_token = None
    if configs.mail_hog_url:
        activation_token = extract_activation_token_from_mailhog(configs.mail_hog_url, email)

    if activation_token:
        try:
            account_api.activate(token=activation_token)
        except requests.HTTPError as exc:
            if exc.response.status_code not in (400, 410):
                pytest.fail(f"Could not activate user {login}: {exc}")

    try:
        logged_in = login_api.login(payload=LoginCredentials(login=login, password=password, remember_me=True))
    except requests.HTTPError as exc:
        pytest.fail(f"Could not login with auto-created user {login}: {exc}")

    token = logged_in.metadata.get("token") if logged_in.metadata else None
    if not token:
        pytest.fail(f"Could not obtain auth token for user {login}")

    return SessionUser(login=login, password=password, email=email, token=token)


@pytest.fixture(scope="session")
def login_api(configs: Config) -> LoginApi:
    return LoginApi(base_url=configs.base_url)


@pytest.fixture(scope="session")
def account_api(configs: Config) -> AccountApi:
    return AccountApi(base_url=configs.base_url)


@pytest.fixture(scope="session")
def session_user(configs: Config, login_api: LoginApi, account_api: AccountApi) -> SessionUser:
    return _create_active_session_user(configs, login_api, account_api, prefix="autotest")


@pytest.fixture(scope="function")
def auth_token(session_user: SessionUser, login_api: LoginApi, fresh_session_user: SessionUser) -> str:
    # Refresh token per test to avoid random 401 when long suite invalidates old session token.
    try:
        logged_in = login_api.login(
            payload=LoginCredentials(
                login=session_user.login,
                password=session_user.password,
                remember_me=True,
            )
        )
        token = logged_in.metadata.get("token") if logged_in.metadata else None
        if token:
            return token
    except requests.HTTPError:
        pass

    return fresh_session_user.token


@pytest.fixture(scope="session")
def user_login(session_user: SessionUser) -> str:
    return session_user.login


@pytest.fixture(scope="session")
def user_password(session_user: SessionUser) -> str:
    return session_user.password


@pytest.fixture(scope="session")
def another_session_user(configs: Config, login_api: LoginApi, account_api: AccountApi) -> SessionUser:
    return _create_active_session_user(configs, login_api, account_api, prefix="autotest_alt")


@pytest.fixture(scope="session")
def another_user_login(another_session_user: SessionUser) -> str:
    return another_session_user.login


@pytest.fixture(scope="function")
def fresh_session_user(configs: Config, login_api: LoginApi, account_api: AccountApi) -> SessionUser:
    return _create_active_session_user(configs, login_api, account_api, prefix="autotest_case")
