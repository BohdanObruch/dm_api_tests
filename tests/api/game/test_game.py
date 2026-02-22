import pytest
import requests

from src.api.models.game.game_model import GameListEnvelope, TagListEnvelope
from tests.fixtures.allure_helpers import step

pytestmark = [pytest.mark.api]


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
        game_api.get_game(id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_delete_game_not_found_returns_410(game_api):
    with step("Delete non-existing game by id"), pytest.raises(requests.HTTPError) as exc_info:
        game_api.delete_game(id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410
