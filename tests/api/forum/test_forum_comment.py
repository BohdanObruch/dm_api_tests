import pytest
import requests
from faker import Faker

from src.api.controllers.forum.comment_controller import CommentController
from tests.fixtures.allure_helpers import step

pytestmark = [pytest.mark.api]

fake = Faker()

@pytest.mark.smoke
def test_get_comment_not_found(forum_comment_api):
    with step("Get comment by non-existing id"):
        non_existent_id = "00000000-0000-0000-0000-000000000000"
        with pytest.raises(requests.HTTPError) as exc_info:
            forum_comment_api.get_comment(id=non_existent_id)
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_get_comment_roundtrip(forum_comment_api, created_comment):
    with step("Get created comment by id"):
        fetched_comment = forum_comment_api.get_comment(id=created_comment.id)
    with step("Verify fetched comment fields"):
        assert fetched_comment.resource is not None
        assert fetched_comment.resource.id == created_comment.id
        assert fetched_comment.resource.text is not None
        assert fetched_comment.resource.text == created_comment.text


@pytest.mark.regression
def test_update_comment_success(forum_comment_api, created_comment):
    with step("Prepare comment update payload"):
        new_text_value = fake.sentence()
        update_payload = {"text": new_text_value}
    with step("Update comment"):
        updated_comment_envelope = forum_comment_api.update_comment(id=created_comment.id, payload=update_payload)
    with step("Verify updated comment response"):
        assert updated_comment_envelope.resource is not None
        assert updated_comment_envelope.resource.id == created_comment.id
        assert updated_comment_envelope.resource.text is not None
        assert updated_comment_envelope.resource.text == new_text_value
    with step("Get updated comment and verify persisted text"):
        fetched_comment = forum_comment_api.get_comment(id=created_comment.id)
        assert fetched_comment.resource is not None
        assert fetched_comment.resource.text is not None
        assert fetched_comment.resource.text == new_text_value


@pytest.mark.regression
def test_update_comment_not_found(forum_comment_api):
    with step("Update non-existing comment"):
        non_existent_id = "00000000-0000-0000-0000-000000000000"
        update_payload = {"text": fake.sentence()}
        with pytest.raises(requests.HTTPError) as exc_info:
            forum_comment_api.update_comment(id=non_existent_id, payload=update_payload)
    with step("Verify status code is 400 or 410"):
        assert exc_info.value.response.status_code in (400, 410)


@pytest.mark.regression
def test_update_comment_invalid_properties(forum_comment_api, created_comment):
    with step("Update comment with invalid payload properties"):
        update_payload = {"text": {"parseMode": "Common"}}
        with pytest.raises(requests.HTTPError) as exc_info:
            forum_comment_api.update_comment(id=created_comment.id, payload=update_payload)
    with step("Verify status code is 400"):
        assert exc_info.value.response.status_code == 400


@pytest.mark.regression
def test_delete_comment_success(topic_api, forum_comment_api, created_topic, valid_comment_payload: dict):
    with step("Create forum comment to delete"):
        comment_envelope = topic_api.post_forum_comment(id=created_topic.id, payload=valid_comment_payload)
        assert comment_envelope.resource is not None
        comment_id = comment_envelope.resource.id
    with step("Delete comment by id"):
        response = forum_comment_api.delete_comment(id=comment_id)
        assert response is None
    with step("Verify deleted comment is not found"):
        with pytest.raises(requests.HTTPError) as exc_info:
            forum_comment_api.get_comment(id=comment_id)
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_delete_comment_not_found(forum_comment_api):
    with step("Delete non-existing comment"):
        non_existent_id = "00000000-0000-0000-0000-000000000000"
        with pytest.raises(requests.HTTPError) as exc_info:
            forum_comment_api.delete_comment(id=non_existent_id)
    with step("Verify status code is 410 or 500"):
        assert exc_info.value.response.status_code in (410, 500)


@pytest.mark.regression
def test_like_comment_success(forum_comment_api, forum_comment_api_liker, created_comment, forum_another_user_login: str):
    with step("Like comment from another user"):
        like_response = forum_comment_api_liker.like_comment(id=created_comment.id)
    with step("Verify like response user"):
        assert like_response.resource is not None
        assert like_response.resource.login == forum_another_user_login
    with step("Get comment and verify like is present"):
        fetched_comment = forum_comment_api.get_comment(id=created_comment.id)
        assert fetched_comment.resource is not None
        assert fetched_comment.resource.likes is not None
        assert any(user.login == forum_another_user_login for user in fetched_comment.resource.likes)


@pytest.mark.regression
def test_like_comment_already_liked(forum_comment_api_liker, created_comment):
    with step("Like comment first time"):
        forum_comment_api_liker.like_comment(id=created_comment.id)
    with step("Like comment second time and verify conflict"):
        with pytest.raises(requests.HTTPError) as exc_info:
            forum_comment_api_liker.like_comment(id=created_comment.id)
        assert exc_info.value.response.status_code == 409


@pytest.mark.regression
def test_like_comment_not_found(forum_comment_api):
    with step("Like non-existing comment"):
        non_existent_id = "00000000-0000-0000-0000-000000000000"
        with pytest.raises(requests.HTTPError) as exc_info:
            forum_comment_api.like_comment(id=non_existent_id)
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_unlike_comment_success(forum_comment_api, forum_comment_api_liker, created_comment, forum_another_user_login: str):
    with step("Like comment before unlike flow"):
        forum_comment_api_liker.like_comment(id=created_comment.id)
    with step("Unlike comment"):
        response = forum_comment_api_liker.unlike_comment(id=created_comment.id)
        assert response is None
    with step("Verify like is removed"):
        fetched_comment = forum_comment_api.get_comment(id=created_comment.id)
        assert fetched_comment.resource is not None
        likes = fetched_comment.resource.likes or []
        assert not any(user.login == forum_another_user_login for user in likes)


@pytest.mark.regression
def test_unlike_comment_not_liked(forum_comment_api_liker, created_comment):
    with step("Unlike comment that is not liked"), pytest.raises(requests.HTTPError) as exc_info:
        forum_comment_api_liker.unlike_comment(id=created_comment.id)
    with step("Verify status code is 409"):
        assert exc_info.value.response.status_code == 409


@pytest.mark.regression
def test_unlike_comment_not_found(forum_comment_api):
    with step("Unlike non-existing comment"):
        non_existent_id = "00000000-0000-0000-0000-000000000000"
        with pytest.raises(requests.HTTPError) as exc_info:
            forum_comment_api.unlike_comment(id=non_existent_id)
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_get_comment_with_render_mode(forum_comment_api, created_comment):
    with step("Get comment with render mode Html"):
        comment_html = forum_comment_api.get_comment(id=created_comment.id, render_mode="Html")
        assert comment_html.resource is not None
        assert comment_html.resource.id == created_comment.id
    with step("Get comment with render mode Text"):
        comment_text = forum_comment_api.get_comment(id=created_comment.id, render_mode="Text")
        assert comment_text.resource is not None
        assert comment_text.resource.id == created_comment.id


@pytest.mark.regression
def test_like_comment_without_token_returns_401_or_403(configs, created_comment):
    api = CommentController(base_url=configs.app_base_url)
    with step("Like comment without auth token"), pytest.raises(requests.HTTPError) as exc_info:
        api.like_comment(id=created_comment.id)
    with step("Verify status code is 401 or 403"):
        assert exc_info.value.response.status_code in (401, 403)


@pytest.mark.regression
def test_update_comment_without_token_returns_401_or_403(configs, created_comment):
    api = CommentController(base_url=configs.app_base_url)
    with step("Update comment without auth token"), pytest.raises(requests.HTTPError) as exc_info:
        api.update_comment(id=created_comment.id, payload={"text": fake.sentence()})
    with step("Verify status code is 401 or 403"):
        assert exc_info.value.response.status_code in (401, 403)
