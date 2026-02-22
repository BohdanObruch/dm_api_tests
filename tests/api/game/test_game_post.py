import pytest
import requests

from tests.fixtures.allure_helpers import step

pytestmark = [pytest.mark.api]


@pytest.mark.regression
def test_get_post_not_found_returns_error(post_api):
    with step("Request non-existing post by id"), pytest.raises(requests.HTTPError) as exc_info:
        post_api.get_post(post_id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410 or 500"):
        assert exc_info.value.response.status_code in (410, 500)
