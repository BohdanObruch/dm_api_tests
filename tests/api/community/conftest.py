from __future__ import annotations

import datetime as dt
import struct
import zlib

import pytest
from faker import Faker

from src.api.controllers.community.poll_controller import PollApi
from src.api.controllers.community.review_controller import ReviewApi
from src.api.controllers.community.user_controller import UserApi
from src.api.controllers.community.userupload_controller import UserUploadApi
from tests.fixtures.api import SessionUser, _create_active_session_user
from tests.fixtures.config import Config

fake = Faker()


def _build_valid_png() -> bytes:
    def _chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
    raw = b"\x00\xff\x00\x00"
    idat = zlib.compress(raw)
    png += _chunk(b"IHDR", ihdr)
    png += _chunk(b"IDAT", idat)
    png += _chunk(b"IEND", b"")
    return png


@pytest.fixture(scope="module")
def community_session_user(configs: Config, login_api, account_api) -> SessionUser:
    return _create_active_session_user(configs, login_api, account_api, prefix="community")


@pytest.fixture(scope="module")
def community_another_session_user(configs: Config, login_api, account_api) -> SessionUser:
    return _create_active_session_user(configs, login_api, account_api, prefix="community_alt")


@pytest.fixture(scope="module")
def community_auth_token(community_session_user: SessionUser) -> str:
    return community_session_user.token


@pytest.fixture(scope="module")
def community_user_login(community_session_user: SessionUser) -> str:
    return community_session_user.login


@pytest.fixture(scope="module")
def community_another_user_login(community_another_session_user: SessionUser) -> str:
    return community_another_session_user.login


@pytest.fixture(scope="function")
def poll_api(configs: Config, community_auth_token: str) -> PollApi:
    return PollApi(base_url=configs.app_base_url, auth_token=community_auth_token)


@pytest.fixture(scope="function")
def review_api(configs: Config, community_auth_token: str) -> ReviewApi:
    return ReviewApi(base_url=configs.app_base_url, auth_token=community_auth_token)


@pytest.fixture(scope="function")
def user_api(configs: Config, community_auth_token: str) -> UserApi:
    return UserApi(base_url=configs.app_base_url, auth_token=community_auth_token)


@pytest.fixture(scope="function")
def user_upload_api(configs: Config, community_auth_token: str) -> UserUploadApi:
    return UserUploadApi(base_url=configs.app_base_url, auth_token=community_auth_token)


@pytest.fixture(scope="function")
def valid_poll_payload() -> dict:
    return {
        "title": fake.sentence(nb_words=4),
        "ends": (dt.datetime.now(dt.UTC) + dt.timedelta(days=3)).isoformat(),
        "options": [
            {"text": fake.sentence(nb_words=2)},
            {"text": fake.sentence(nb_words=2)},
        ],
    }


@pytest.fixture(scope="function")
def valid_review_payload() -> dict:
    # API expects BbText serialized as a simple string in this environment.
    return {
        "text": fake.sentence(nb_words=6),
        "approved": False,
    }


@pytest.fixture(scope="function")
def valid_png_bytes() -> bytes:
    return _build_valid_png()
