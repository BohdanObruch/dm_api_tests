from __future__ import annotations

import pytest
import requests
from faker import Faker

from src.api.controllers.forum.topic_controller import TopicController
from src.api.models.forum.topic_model import Comment, CommentListEnvelope, Topic, TopicEnvelope
from tests.fixtures.allure_helpers import step

pytestmark = [pytest.mark.api]

fake = Faker()


@pytest.mark.smoke
def test_get_topic_not_found(topic_api):
    with step("Get topic by non-existing id"):
        non_existent_topic_id = "00000000-0000-0000-0000-000000000000"
        with pytest.raises(requests.HTTPError) as excinfo:
            topic_api.get_topic(id=non_existent_topic_id)
    with step("Verify status code is 410"):
        assert excinfo.value.response.status_code == 410


@pytest.mark.regression
def test_create_and_get_topic_roundtrip(topic_api, created_topic: Topic):
    with step("Get created topic by id"):
        topic_envelope = topic_api.get_topic(id=created_topic.id)
    with step("Verify topic response"):
        assert isinstance(topic_envelope, TopicEnvelope)
        assert topic_envelope.resource is not None
        assert topic_envelope.resource.id == created_topic.id


@pytest.mark.regression
def test_put_topic_roundtrip(topic_api, created_topic: Topic):
    with step("Prepare topic update payload"):
        new_title = fake.sentence(nb_words=5)
        payload = {
            "title": new_title,
            "description": fake.paragraph(nb_sentences=2),
            "attached": created_topic.attached if created_topic.attached is not None else False,
            "closed": created_topic.closed if created_topic.closed is not None else False,
        }
    with step("Update topic by id"):
        updated_topic_envelope = topic_api.put_topic(id=created_topic.id, payload=payload)
    with step("Verify updated topic fields"):
        assert updated_topic_envelope.resource is not None
        assert updated_topic_envelope.resource.id == created_topic.id
        assert updated_topic_envelope.resource.title == new_title
        assert updated_topic_envelope.resource.description is not None
        assert updated_topic_envelope.resource.description == payload["description"]


@pytest.mark.regression
def test_like_and_unlike_topic(topic_api_liker, created_topic: Topic, forum_another_user_login: str):
    with step("Like topic"):
        like_envelope = topic_api_liker.post_topic_like(id=created_topic.id)
    with step("Verify like response user"):
        assert like_envelope.resource is not None
        assert like_envelope.resource.login == forum_another_user_login
    with step("Unlike topic"):
        response = topic_api_liker.delete_topic_like(id=created_topic.id)
        assert response is None
    with step("Unlike topic second time and verify conflict"):
        with pytest.raises(requests.HTTPError) as excinfo:
            topic_api_liker.delete_topic_like(id=created_topic.id)
        assert excinfo.value.response.status_code == 409


@pytest.mark.regression
def test_get_forum_comments(topic_api, created_topic: Topic):
    with step("Get comments for topic"):
        comment_list_envelope = topic_api.get_forum_comments(id=created_topic.id, size=10)
    with step("Verify topic comments response"):
        assert isinstance(comment_list_envelope, CommentListEnvelope)
        assert comment_list_envelope.resources is None or isinstance(comment_list_envelope.resources, list)
        if comment_list_envelope.resources:
            assert all(isinstance(comment, Comment) for comment in comment_list_envelope.resources)


@pytest.mark.regression
def test_post_comment_and_read_comments(topic_api, created_topic: Topic, valid_comment_payload: dict):
    with step("Post comment to topic"):
        created_comment_envelope = topic_api.post_forum_comment(id=created_topic.id, payload=valid_comment_payload)
        created_comment = created_comment_envelope.resource
    with step("Verify created comment payload"):
        assert created_comment is not None
        assert created_comment.id is not None
        assert created_comment.text is not None
        assert created_comment.text == valid_comment_payload["text"]
    with step("Get topic comments and verify new comment is present"):
        comment_list_envelope = topic_api.get_forum_comments(id=created_topic.id, size=20)
        assert comment_list_envelope.resources is not None
        assert any(comment.id == created_comment.id for comment in comment_list_envelope.resources)
    with step("Read topic comments"):
        read_response = topic_api.read_topic_comments(id=created_topic.id)
        assert read_response is None


@pytest.mark.regression
def test_put_topic_not_found(topic_api):
    with step("Update topic by non-existing id"):
        non_existent_topic_id = "00000000-0000-0000-0000-000000000000"
        payload = {"title": fake.sentence()}
        with pytest.raises(requests.HTTPError) as excinfo:
            topic_api.put_topic(id=non_existent_topic_id, payload=payload)
    with step("Verify status code is 400 or 410"):
        assert excinfo.value.response.status_code in (400, 410)


@pytest.mark.regression
def test_delete_topic_not_found(topic_api):
    with step("Delete topic by non-existing id"):
        non_existent_topic_id = "00000000-0000-0000-0000-000000000000"
        with pytest.raises(requests.HTTPError) as excinfo:
            topic_api.delete_topic(id=non_existent_topic_id)
    with step("Verify status code is 410"):
        assert excinfo.value.response.status_code == 410


@pytest.mark.regression
def test_post_topic_like_not_found(topic_api):
    with step("Like topic by non-existing id"):
        non_existent_topic_id = "00000000-0000-0000-0000-000000000000"
        with pytest.raises(requests.HTTPError) as excinfo:
            topic_api.post_topic_like(id=non_existent_topic_id)
    with step("Verify status code is 410"):
        assert excinfo.value.response.status_code == 410


@pytest.mark.regression
def test_delete_topic_like_not_found(topic_api):
    with step("Delete topic like by non-existing id"):
        non_existent_topic_id = "00000000-0000-0000-0000-000000000000"
        with pytest.raises(requests.HTTPError) as excinfo:
            topic_api.delete_topic_like(id=non_existent_topic_id)
    with step("Verify status code is 410"):
        assert excinfo.value.response.status_code == 410


@pytest.mark.regression
def test_get_forum_comments_not_found(topic_api):
    with step("Get forum comments by non-existing topic id"):
        non_existent_topic_id = "00000000-0000-0000-0000-000000000000"
        with pytest.raises(requests.HTTPError) as excinfo:
            topic_api.get_forum_comments(id=non_existent_topic_id)
    with step("Verify status code is 410"):
        assert excinfo.value.response.status_code == 410


@pytest.mark.regression
def test_post_forum_comment_not_found(topic_api):
    with step("Post forum comment to non-existing topic"):
        non_existent_topic_id = "00000000-0000-0000-0000-000000000000"
        payload = {"text": fake.sentence()}
        with pytest.raises(requests.HTTPError) as excinfo:
            topic_api.post_forum_comment(id=non_existent_topic_id, payload=payload)
    with step("Verify status code is 400 or 410"):
        assert excinfo.value.response.status_code in (400, 410)


@pytest.mark.regression
def test_read_topic_comments_not_found(topic_api):
    with step("Read topic comments for non-existing topic"):
        non_existent_topic_id = "00000000-0000-0000-0000-000000000000"
        with pytest.raises(requests.HTTPError) as excinfo:
            topic_api.read_topic_comments(id=non_existent_topic_id)
    with step("Verify status code is 410"):
        assert excinfo.value.response.status_code == 410


@pytest.mark.regression
def test_post_topic_like_without_token_returns_401_or_403(configs, created_topic: Topic):
    api = TopicController(base_url=configs.app_base_url)
    with step("Like topic without auth token"), pytest.raises(requests.HTTPError) as excinfo:
        api.post_topic_like(id=created_topic.id)
    with step("Verify status code is 401 or 403"):
        assert excinfo.value.response.status_code in (401, 403)


@pytest.mark.regression
def test_post_forum_comment_without_token_returns_401_or_403(configs, created_topic: Topic):
    api = TopicController(base_url=configs.app_base_url)
    payload = {"text": fake.sentence()}
    with step("Post topic comment without auth token"), pytest.raises(requests.HTTPError) as excinfo:
        api.post_forum_comment(id=created_topic.id, payload=payload)
    with step("Verify status code is 401 or 403"):
        assert excinfo.value.response.status_code in (401, 403)
