from __future__ import annotations

import pytest
import requests
from faker import Faker

from src.api.controllers.forum.comment_controller import CommentController
from src.api.controllers.forum.forum_controller import ForumApi
from src.api.controllers.forum.topic_controller import TopicController
from src.api.models.forum.comment_model import Comment
from src.api.models.forum.topic_model import Topic
from tests.fixtures.api import SessionUser, _create_active_session_user
from tests.fixtures.config import Config

fake = Faker()


@pytest.fixture(scope="module")
def forum_session_user(configs: Config, login_api, account_api) -> SessionUser:
    return _create_active_session_user(configs, login_api, account_api, prefix="forum")


@pytest.fixture(scope="module")
def forum_auth_token(forum_session_user: SessionUser) -> str:
    return forum_session_user.token


@pytest.fixture(scope="module")
def forum_another_session_user(configs: Config, login_api, account_api) -> SessionUser:
    return _create_active_session_user(configs, login_api, account_api, prefix="forum_alt")


@pytest.fixture(scope="module")
def forum_another_auth_token(forum_another_session_user: SessionUser) -> str:
    return forum_another_session_user.token


@pytest.fixture(scope="module")
def forum_user_login(forum_session_user: SessionUser) -> str:
    return forum_session_user.login


@pytest.fixture(scope="module")
def forum_another_user_login(forum_another_session_user: SessionUser) -> str:
    return forum_another_session_user.login


@pytest.fixture(scope="function")
def forum_api(configs: Config, forum_auth_token: str) -> ForumApi:
    return ForumApi(base_url=configs.app_base_url, auth_token=forum_auth_token)


@pytest.fixture(scope="function")
def topic_api(configs: Config, forum_auth_token: str) -> TopicController:
    return TopicController(base_url=configs.app_base_url, auth_token=forum_auth_token)


@pytest.fixture(scope="function")
def topic_api_liker(configs: Config, forum_another_auth_token: str) -> TopicController:
    return TopicController(base_url=configs.app_base_url, auth_token=forum_another_auth_token)


@pytest.fixture(scope="function")
def forum_comment_api(configs: Config, forum_auth_token: str) -> CommentController:
    return CommentController(base_url=configs.app_base_url, auth_token=forum_auth_token)


@pytest.fixture(scope="function")
def forum_comment_api_liker(configs: Config, forum_another_auth_token: str) -> CommentController:
    return CommentController(base_url=configs.app_base_url, auth_token=forum_another_auth_token)


@pytest.fixture(scope="function")
def valid_forum_id(forum_api: ForumApi) -> str:
    fora = forum_api.get_fora()
    if not fora.resources:
        pytest.skip("No fora available for forum tests.")
    forum_id = fora.resources[0].id
    if not forum_id:
        pytest.skip("Forum id is missing in API response.")
    return forum_id


@pytest.fixture(scope="function")
def valid_topic_payload() -> dict:
    return {
        "title": fake.sentence(nb_words=6),
        "description": fake.paragraph(nb_sentences=2),
    }


@pytest.fixture(scope="function")
def valid_comment_payload() -> dict:
    return {
        "text": fake.sentence(nb_words=8),
    }


@pytest.fixture(scope="function")
def created_topic(forum_api: ForumApi, topic_api: TopicController, valid_forum_id: str, valid_topic_payload: dict) -> Topic:
    created_envelope = forum_api.post_topic(id=valid_forum_id, payload=valid_topic_payload)

    created = created_envelope.resource
    if created is None or not created.id:
        pytest.skip("Topic was not created or id is missing in response.")

    yield created

    try:
        topic_api.delete_topic(id=created.id)
    except requests.HTTPError as exc:
        if exc.response is None or exc.response.status_code not in (403, 404, 410):
            raise


@pytest.fixture(scope="function")
def created_comment(
    topic_api: TopicController,
    forum_comment_api: CommentController,
    created_topic: Topic,
    valid_comment_payload: dict,
) -> Comment:
    created_envelope = topic_api.post_forum_comment(id=created_topic.id, payload=valid_comment_payload)

    created = created_envelope.resource
    if created is None or not created.id:
        pytest.skip("Comment was not created or id is missing in response.")

    yield created

    try:
        forum_comment_api.delete_comment(id=created.id)
    except requests.HTTPError as exc:
        if exc.response is None or exc.response.status_code not in (403, 404, 410):
            raise
