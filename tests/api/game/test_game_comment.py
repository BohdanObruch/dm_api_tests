import pytest
import requests

from src.api.controllers.game.comment_controller import CommentApi
from tests.fixtures.allure_helpers import step


@pytest.mark.regression
def test_get_game_comment_not_found_returns_410(comment_api):
    with step("Request non-existing game comment by id"), pytest.raises(requests.HTTPError) as exc_info:
        comment_api.get_game_comment(comment_id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_delete_game_comment_not_found_returns_410(comment_api):
    with step("Delete non-existing game comment by id"), pytest.raises(requests.HTTPError) as exc_info:
        comment_api.delete_game_comment(comment_id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_get_game_comments_for_non_existing_game_returns_410(comment_api):
    with step("Request comments for non-existing game"), pytest.raises(requests.HTTPError) as exc_info:
        comment_api.get_game_comments(game_id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_read_game_comments_for_non_existing_game_returns_410(comment_api):
    with step("Mark comments as read for non-existing game"), pytest.raises(requests.HTTPError) as exc_info:
        comment_api.read_game_comments(game_id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_like_game_comment_not_found_returns_410(comment_api):
    with step("Like non-existing game comment"), pytest.raises(requests.HTTPError) as exc_info:
        comment_api.post_game_comment_like(comment_id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_get_game_comment_without_token_returns_401_or_403(configs):
    api = CommentApi(base_url=configs.app_base_url)
    with step("Get game comment without auth token"), pytest.raises(requests.HTTPError) as exc_info:
        api.get_game_comment(comment_id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 401, 403, or 410"):
        assert exc_info.value.response.status_code in (401, 403, 410)


@pytest.mark.regression
def test_delete_game_comment_without_token_returns_401_or_403(configs):
    api = CommentApi(base_url=configs.app_base_url)
    with step("Delete game comment without auth token"), pytest.raises(requests.HTTPError) as exc_info:
        api.delete_game_comment(comment_id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 401 or 403"):
        assert exc_info.value.response.status_code in (401, 403)
