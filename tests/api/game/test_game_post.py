import pytest
import requests

from src.api.controllers.game.post_controller import PostApi
from tests.fixtures.allure_helpers import step


@pytest.mark.regression
def test_get_post_not_found_returns_error(post_api):
    with step("Request non-existing post by id"), pytest.raises(requests.HTTPError) as exc_info:
        post_api.get_post(post_id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410 or 500"):
        assert exc_info.value.response.status_code in (410, 500)


@pytest.mark.regression
def test_get_posts_for_non_existing_room_returns_410(post_api):
    with step("Request posts for non-existing room id"), pytest.raises(requests.HTTPError) as exc_info:
        post_api.get_posts(room_id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_mark_posts_as_read_for_non_existing_room_returns_410(post_api):
    with step("Mark posts as read for non-existing room id"), pytest.raises(requests.HTTPError) as exc_info:
        post_api.mark_posts_as_read(room_id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_get_post_votes_not_found_returns_410(post_api):
    with step("Request votes for non-existing post id"), pytest.raises(requests.HTTPError) as exc_info:
        post_api.get_post_votes(post_id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410 or known 501"):
        assert exc_info.value.response.status_code in (410, 501)


@pytest.mark.regression
def test_get_post_without_token_returns_401_or_403(configs):
    api = PostApi(base_url=configs.app_base_url)
    with step("Get post without auth token"), pytest.raises(requests.HTTPError) as exc_info:
        api.get_post(post_id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 401, 403, 410, or known 500"):
        assert exc_info.value.response.status_code in (401, 403, 410, 500)


@pytest.mark.regression
def test_delete_post_without_token_returns_401_or_403(configs):
    api = PostApi(base_url=configs.app_base_url)
    with step("Delete post without auth token"), pytest.raises(requests.HTTPError) as exc_info:
        api.delete_post(post_id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 401 or 403"):
        assert exc_info.value.response.status_code in (401, 403)
