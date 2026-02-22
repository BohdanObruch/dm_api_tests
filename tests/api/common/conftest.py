from __future__ import annotations

import pytest

from src.api.controllers.common.search_controller import SearchApi
from tests.fixtures.config import Config


@pytest.fixture(scope="function")
def search_api(configs: Config, auth_token: str) -> SearchApi:
    return SearchApi(base_url=configs.app_base_url, auth_token=auth_token)
