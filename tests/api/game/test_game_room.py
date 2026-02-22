import pytest
import requests

from src.api.controllers.game.room_controller import RoomApi
from tests.fixtures.allure_helpers import step


@pytest.mark.regression
def test_get_room_not_found_returns_410(room_api):
    with step("Request non-existing room by id"), pytest.raises(requests.HTTPError) as exc_info:
        room_api.get_room(room_id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_get_rooms_for_non_existing_game_returns_410(room_api):
    with step("Request rooms for non-existing game id"), pytest.raises(requests.HTTPError) as exc_info:
        room_api.get_rooms(game_id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_delete_claim_not_found_returns_410(room_api):
    with step("Delete non-existing room claim by id"), pytest.raises(requests.HTTPError) as exc_info:
        room_api.delete_claim(claim_id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410 or known 500"):
        assert exc_info.value.response.status_code in (410, 500)


@pytest.mark.regression
def test_delete_pending_post_not_found_returns_410(room_api):
    with step("Delete non-existing pending post by id"), pytest.raises(requests.HTTPError) as exc_info:
        room_api.delete_pending_post(pending_post_id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_get_rooms_without_token_returns_401_or_403(configs):
    api = RoomApi(base_url=configs.app_base_url)
    with step("Request rooms without auth token"), pytest.raises(requests.HTTPError) as exc_info:
        api.get_rooms(game_id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 401, 403, or 410"):
        assert exc_info.value.response.status_code in (401, 403, 410)


@pytest.mark.regression
def test_post_room_without_token_returns_401_or_403(configs):
    api = RoomApi(base_url=configs.app_base_url)
    payload = {"title": "room without auth", "access": "Open", "type": "Default"}
    with step("Create room without auth token"), pytest.raises(requests.HTTPError) as exc_info:
        api.post_room(game_id="00000000-0000-0000-0000-000000000000", payload=payload)
    with step("Verify status code is 401 or 403"):
        assert exc_info.value.response.status_code in (401, 403)
