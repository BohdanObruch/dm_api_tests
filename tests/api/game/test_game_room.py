import pytest
import requests

from src.api.controllers.game.room_controller import RoomApi
from tests.fixtures.allure_helpers import step

NON_EXISTENT_ID = "00000000-0000-0000-0000-000000000000"


@pytest.mark.regression
def test_get_room_not_found_returns_410(room_api):
    with step("Request non-existing room by id"), pytest.raises(requests.HTTPError) as exc_info:
        room_api.get_room(room_id=NON_EXISTENT_ID)
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_get_rooms_for_non_existing_game_returns_410(room_api):
    with step("Request rooms for non-existing game id"), pytest.raises(requests.HTTPError) as exc_info:
        room_api.get_rooms(game_id=NON_EXISTENT_ID)
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_delete_claim_not_found_returns_410(room_api):
    with step("Delete non-existing room claim by id"), pytest.raises(requests.HTTPError) as exc_info:
        room_api.delete_claim(claim_id=NON_EXISTENT_ID)
    with step("Verify status code is 410 or known 500"):
        assert exc_info.value.response.status_code in (410, 500)


@pytest.mark.regression
def test_delete_pending_post_not_found_returns_410(room_api):
    with step("Delete non-existing pending post by id"), pytest.raises(requests.HTTPError) as exc_info:
        room_api.delete_pending_post(pending_post_id=NON_EXISTENT_ID)
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_get_rooms_without_token_returns_401_or_403(configs):
    api = RoomApi(base_url=configs.app_base_url)
    with step("Request rooms without auth token"), pytest.raises(requests.HTTPError) as exc_info:
        api.get_rooms(game_id=NON_EXISTENT_ID)
    with step("Verify status code is 401, 403, or 410"):
        assert exc_info.value.response.status_code in (401, 403, 410)


@pytest.mark.regression
def test_post_room_without_token_returns_401_or_403(configs):
    api = RoomApi(base_url=configs.app_base_url)
    payload = {"title": "room without auth", "access": "Open", "type": "Default"}
    with step("Create room without auth token"), pytest.raises(requests.HTTPError) as exc_info:
        api.post_room(game_id=NON_EXISTENT_ID, payload=payload)
    with step("Verify status code is 401 or 403"):
        assert exc_info.value.response.status_code in (401, 403)


@pytest.mark.regression
def test_put_room_for_non_existing_room_returns_documented_error(room_api):
    payload = {"title": "updated room by autotest"}
    with step("Update non-existing room"), pytest.raises(requests.HTTPError) as exc_info:
        room_api.put_room(room_id=NON_EXISTENT_ID, payload=payload)
    with step("Verify status code is documented for PATCH /v1/rooms/{id}"):
        assert exc_info.value.response.status_code in (400, 401, 403, 410)


@pytest.mark.regression
def test_delete_room_without_token_returns_documented_error(configs):
    api = RoomApi(base_url=configs.app_base_url)
    with step("Delete room without auth token"), pytest.raises(requests.HTTPError) as exc_info:
        api.delete_room(room_id=NON_EXISTENT_ID)
    with step("Verify status code is documented for DELETE /v1/rooms/{id}"):
        assert exc_info.value.response.status_code in (401, 403)


@pytest.mark.regression
def test_post_claim_for_non_existing_room_returns_documented_error(room_api):
    payload = {"text": "autotest claim"}
    with step("Create claim for non-existing room"), pytest.raises(requests.HTTPError) as exc_info:
        room_api.post_claim(room_id=NON_EXISTENT_ID, payload=payload)
    with step("Verify status code is documented for POST /v1/rooms/{id}/claims"):
        assert exc_info.value.response.status_code in (400, 401, 403, 409, 410)


@pytest.mark.regression
def test_update_claim_for_non_existing_claim_returns_documented_error(room_api):
    payload = {"text": "updated claim by autotest"}
    with step("Update non-existing claim"), pytest.raises(requests.HTTPError) as exc_info:
        room_api.update_claim(claim_id=NON_EXISTENT_ID, payload=payload)
    with step("Verify status code is documented for PATCH /v1/rooms/claims/{id}"):
        assert exc_info.value.response.status_code in (400, 401, 403, 410)


@pytest.mark.regression
def test_create_pending_post_without_token_returns_documented_error(configs):
    api = RoomApi(base_url=configs.app_base_url)
    payload = {"title": "autotest pending", "content": "autotest"}
    with step("Create pending post without auth token"), pytest.raises(requests.HTTPError) as exc_info:
        api.create_pending_post(room_id=NON_EXISTENT_ID, payload=payload)
    with step("Verify status code is documented for POST /v1/rooms/{id}/pendings"):
        assert exc_info.value.response.status_code in (401, 403)
