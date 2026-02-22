from __future__ import annotations

import pytest

from src.api.controllers.messaging.chat_controller import ChatApi
from src.api.controllers.messaging.messaging_controller import MessagingApi
from tests.fixtures.config import Config


@pytest.fixture(scope="function")
def messaging_api(configs: Config, auth_token: str) -> MessagingApi:
    return MessagingApi(base_url=configs.app_base_url, auth_token=auth_token)


@pytest.fixture(scope="function")
def chat_api(configs: Config, auth_token: str) -> ChatApi:
    return ChatApi(base_url=configs.app_base_url, auth_token=auth_token)
