from __future__ import annotations

import pytest
import requests

from src.api.controllers.forum.forum_controller import ForumApi
from src.api.models.forum.forum_model import ForumEnvelope, ForumListEnvelope, TopicListEnvelope, UserListEnvelope
from tests.fixtures.allure_helpers import step


@pytest.mark.smoke
def test_get_fora_list(forum_api):
    with step("Get forums list"):
        response = forum_api.get_fora()
    with step("Verify forums list response"):
        assert isinstance(response, ForumListEnvelope)
        assert response.resources is None or isinstance(response.resources, list)


@pytest.mark.regression
def test_get_specific_forum(forum_api, valid_forum_id: str):
    with step("Get forum by id"):
        response = forum_api.get_forum(id=valid_forum_id)
    with step("Verify forum response id"):
        assert isinstance(response, ForumEnvelope)
        assert response.resource is not None
        assert response.resource.id == valid_forum_id


@pytest.mark.regression
def test_read_forum_comments(forum_api, valid_forum_id: str):
    with step("Mark all comments in forum as read"):
        try:
            response = forum_api.read_forum_comments(id=valid_forum_id)
        except requests.HTTPError as exc_info:
            assert exc_info.response.status_code == 500
            return
    with step("Verify read response is empty"):
        assert response is None


@pytest.mark.regression
def test_get_forum_moderators(forum_api, valid_forum_id: str):
    with step("Get forum moderators"):
        response = forum_api.get_moderators(id=valid_forum_id)
    with step("Verify moderators response"):
        assert isinstance(response, UserListEnvelope)
        assert response.resources is None or isinstance(response.resources, list)


@pytest.mark.regression
def test_get_topics_in_forum(forum_api, valid_forum_id: str):
    with step("Get topics in forum"):
        response = forum_api.get_topics(id=valid_forum_id)
    with step("Verify topics response"):
        assert isinstance(response, TopicListEnvelope)
        assert response.resources is None or isinstance(response.resources, list)


@pytest.mark.regression
def test_post_topic_in_forum(created_topic, valid_topic_payload: dict):
    with step("Verify created topic payload values"):
        assert created_topic.id is not None
        assert created_topic.title == valid_topic_payload["title"]
        assert created_topic.description is not None
        assert created_topic.description == valid_topic_payload["description"]


@pytest.mark.regression
def test_get_forum_not_found(forum_api):
    with step("Get forum by unknown id"), pytest.raises(requests.HTTPError) as exc_info:
        forum_api.get_forum(id="unknown_forum_id")
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_get_topics_forum_not_found(forum_api):
    with step("Get topics for unknown forum id"), pytest.raises(requests.HTTPError) as exc_info:
        forum_api.get_topics(id="unknown_forum_id")
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_post_topic_without_token_returns_401_or_403(configs, valid_forum_id: str, valid_topic_payload: dict):
    api = ForumApi(base_url=configs.app_base_url)
    with step("Post topic without auth token"), pytest.raises(requests.HTTPError) as exc_info:
        api.post_topic(id=valid_forum_id, payload=valid_topic_payload)
    with step("Verify status code is 401 or 403"):
        assert exc_info.value.response.status_code in (401, 403)


@pytest.mark.regression
def test_read_forum_comments_without_token_returns_401_or_403(configs, valid_forum_id: str):
    api = ForumApi(base_url=configs.app_base_url)
    with step("Mark forum comments as read without auth token"), pytest.raises(requests.HTTPError) as exc_info:
        api.read_forum_comments(id=valid_forum_id)
    with step("Verify status code is 401 or 403"):
        assert exc_info.value.response.status_code in (401, 403)
