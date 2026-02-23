import pytest
import requests

from src.api.controllers.game.game_controller import GameApi
from src.api.models.game.game_model import GameListEnvelope, TagListEnvelope
from tests.fixtures.allure_helpers import step

NON_EXISTENT_ID = "00000000-0000-0000-0000-000000000000"


@pytest.mark.smoke
def test_get_games_list(game_api):
    with step("Get games list"):
        response = game_api.get_games()
    with step("Verify games list response"):
        assert isinstance(response, GameListEnvelope)
        assert response.resources is None or isinstance(response.resources, list)


@pytest.mark.regression
def test_get_games_with_status_filter(game_api):
    with step("Get games list filtered by status Active"):
        response = game_api.get_games(statuses=["Active"])
    with step("Verify filtered games response"):
        assert isinstance(response, GameListEnvelope)
        assert response.resources is None or isinstance(response.resources, list)


@pytest.mark.regression
def test_get_popular_games(game_api):
    with step("Get popular games"):
        response = game_api.get_popular_games()
    with step("Verify popular games response"):
        assert isinstance(response, GameListEnvelope)
        assert response.resources is None or isinstance(response.resources, list)


@pytest.mark.regression
def test_get_own_games(game_api):
    with step("Get own games"):
        response = game_api.get_own_games()
    with step("Verify own games response"):
        assert isinstance(response, GameListEnvelope)
        assert response.resources is None or isinstance(response.resources, list)


@pytest.mark.regression
def test_get_tags(game_api):
    with step("Get tags"):
        response = game_api.get_tags()
    with step("Verify tags response"):
        assert isinstance(response, TagListEnvelope)
        assert response.resources is None or isinstance(response.resources, list)


@pytest.mark.regression
def test_get_game_not_found_returns_410(game_api):
    with step("Request non-existing game by id"), pytest.raises(requests.HTTPError) as exc_info:
        game_api.get_game(id=NON_EXISTENT_ID)
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_delete_game_not_found_returns_410(game_api):
    with step("Delete non-existing game by id"), pytest.raises(requests.HTTPError) as exc_info:
        game_api.delete_game(id=NON_EXISTENT_ID)
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_get_own_games_without_token_returns_401_or_403(configs):
    api = GameApi(base_url=configs.app_base_url)
    with step("Get own games without auth token"), pytest.raises(requests.HTTPError) as exc_info:
        api.get_own_games()
    with step("Verify status code is 401 or 403"):
        assert exc_info.value.response.status_code in (401, 403)


@pytest.mark.regression
def test_get_game_details_not_found_returns_410(game_api):
    with step("Request non-existing game details by id"), pytest.raises(requests.HTTPError) as exc_info:
        game_api.get_game_details(id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_get_game_readers_not_found_returns_410(game_api):
    with step("Request readers for non-existing game"), pytest.raises(requests.HTTPError) as exc_info:
        game_api.get_readers(id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_get_game_blacklist_not_found_returns_410(game_api):
    with step("Request blacklist for non-existing game"), pytest.raises(requests.HTTPError) as exc_info:
        game_api.get_blacklist(id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_post_reader_without_token_returns_401_or_403(configs):
    api = GameApi(base_url=configs.app_base_url)
    with step("Add reader without auth token"), pytest.raises(requests.HTTPError) as exc_info:
        api.post_reader(id=NON_EXISTENT_ID)
    with step("Verify status code is 401 or 403"):
        assert exc_info.value.response.status_code in (401, 403)


@pytest.mark.regression
def test_delete_reader_without_token_returns_401_or_403(configs):
    api = GameApi(base_url=configs.app_base_url)
    with step("Delete reader without auth token"), pytest.raises(requests.HTTPError) as exc_info:
        api.delete_reader(id=NON_EXISTENT_ID)
    with step("Verify status code is 401 or 403"):
        assert exc_info.value.response.status_code in (401, 403)


@pytest.mark.regression
def test_post_blacklist_without_token_returns_401_or_403(configs):
    api = GameApi(base_url=configs.app_base_url)
    with step("Add blacklist record without auth token"), pytest.raises(requests.HTTPError) as exc_info:
        api.post_blacklist(id=NON_EXISTENT_ID, payload={"login": "non_existent_user"})
    with step("Verify status code is 401 or 403"):
        assert exc_info.value.response.status_code in (401, 403)


@pytest.mark.regression
def test_post_game_without_token_returns_documented_error(configs):
    api = GameApi(base_url=configs.app_base_url)
    payload = {"title": "autotest game"}
    with step("Create game without auth token"), pytest.raises(requests.HTTPError) as exc_info:
        api.post_game(payload=payload)
    with step("Verify status code is documented for POST /v1/games"):
        assert exc_info.value.response.status_code in (400, 401, 403, 410)


@pytest.mark.regression
def test_put_game_details_for_non_existing_game_returns_documented_error(game_api):
    payload = {"title": "updated by autotest"}
    with step("Update details for non-existing game"), pytest.raises(requests.HTTPError) as exc_info:
        game_api.put_game(id=NON_EXISTENT_ID, payload=payload)
    with step("Verify status code is documented for PATCH /v1/games/{id}/details"):
        assert exc_info.value.response.status_code in (400, 401, 403, 410)


@pytest.mark.regression
def test_delete_blacklist_without_token_returns_documented_error(configs):
    api = GameApi(base_url=configs.app_base_url)
    with step("Delete blacklist entry without auth token"), pytest.raises(requests.HTTPError) as exc_info:
        api.delete_blacklist(id=NON_EXISTENT_ID, login="non_existent_user")
    with step("Verify status code is documented for DELETE /v1/games/{id}/blacklist/users/{login}"):
        assert exc_info.value.response.status_code in (401, 403)
