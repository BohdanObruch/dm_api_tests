import pytest
import requests

from tests.fixtures.allure_helpers import step

pytestmark = [pytest.mark.api]


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
