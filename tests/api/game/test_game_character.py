import pytest
import requests

from tests.fixtures.allure_helpers import step

pytestmark = [pytest.mark.api]


@pytest.mark.regression
def test_get_character_not_found_returns_410(character_api):
    with step("Request non-existing character by id"), pytest.raises(requests.HTTPError) as exc_info:
        character_api.get_character(id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410
