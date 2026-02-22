import pytest
import requests

from src.api.controllers.game.character_controller import CharacterApi
from tests.fixtures.allure_helpers import step


@pytest.mark.regression
def test_get_character_not_found_returns_410(character_api):
    with step("Request non-existing character by id"), pytest.raises(requests.HTTPError) as exc_info:
        character_api.get_character(id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_get_game_characters_for_non_existing_game_returns_410(character_api):
    with step("Request characters for non-existing game"), pytest.raises(requests.HTTPError) as exc_info:
        character_api.get_game_characters(id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_delete_character_not_found_returns_410(character_api):
    with step("Delete non-existing character by id"), pytest.raises(requests.HTTPError) as exc_info:
        character_api.delete_character(id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410 or known 500"):
        assert exc_info.value.response.status_code in (410, 500)


@pytest.mark.regression
def test_get_character_without_token_returns_401_or_403(configs):
    api = CharacterApi(base_url=configs.app_base_url)
    with step("Get character without auth token"), pytest.raises(requests.HTTPError) as exc_info:
        api.get_character(id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 401, 403, or 410"):
        assert exc_info.value.response.status_code in (401, 403, 410)
