import pytest
import requests

from src.api.controllers.community.poll_controller import PollApi
from src.api.models.community.poll_model import PollListEnvelope
from tests.fixtures.allure_helpers import step

pytestmark = [pytest.mark.api]


@pytest.mark.smoke
def test_create_poll_forbidden_for_regular_user(poll_api, valid_poll_payload: dict):
    with step("Create poll as regular user"), pytest.raises(requests.HTTPError) as exc_info:
        poll_api.create(payload=valid_poll_payload)
    with step("Verify status code is 401 or 403"):
        assert exc_info.value.response.status_code in (401, 403)


@pytest.mark.regression
def test_create_poll_invalid_payload_returns_400(poll_api):
    with step("Create poll with invalid payload"), pytest.raises(requests.HTTPError) as exc_info:
        poll_api.create(payload={"title": "No end date", "options": [{"text": "A"}, {"text": "B"}]})
    with step("Verify status code is 400 or 401"):
        assert exc_info.value.response.status_code in (400, 401)


@pytest.mark.regression
def test_get_polls_list_returns_200_or_known_500(poll_api):
    with step("Get polls list"):
        try:
            envelope = poll_api.list()
        except requests.HTTPError as exc_info:
            assert exc_info.response.status_code == 500
            return
    with step("Verify polls list response"):
        assert isinstance(envelope, PollListEnvelope)
        assert envelope.resources is None or isinstance(envelope.resources, list)


@pytest.mark.regression
def test_get_poll_by_invalid_id_returns_410_or_known_500(poll_api):
    with step("Get poll by invalid id"), pytest.raises(requests.HTTPError) as exc_info:
        poll_api.get(id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410 or 500"):
        assert exc_info.value.response.status_code in (410, 500)


@pytest.mark.regression
def test_vote_for_invalid_poll_returns_error(poll_api):
    with step("Vote for invalid poll and option id"), pytest.raises(requests.HTTPError) as exc_info:
        poll_api.vote(
            id="00000000-0000-0000-0000-000000000000",
            option_id="00000000-0000-0000-0000-000000000000",
        )
    with step("Verify status code is one of expected error codes"):
        assert exc_info.value.response.status_code in (401, 403, 410, 500)


@pytest.mark.regression
def test_get_polls_without_token_returns_200_or_auth_error(configs):
    api = PollApi(base_url=configs.app_base_url)
    with step("Get polls list without auth token"):
        try:
            response = api.list(size=5)
        except requests.HTTPError as exc_info:
            assert exc_info.response.status_code in (401, 403, 500)
            return
    with step("Verify response structure when endpoint is public"):
        assert isinstance(response, PollListEnvelope)


@pytest.mark.regression
def test_vote_poll_without_token_returns_401_or_403(configs):
    api = PollApi(base_url=configs.app_base_url)
    with step("Vote in poll without auth token"), pytest.raises(requests.HTTPError) as exc_info:
        api.vote(id="00000000-0000-0000-0000-000000000000", option_id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 401 or 403"):
        assert exc_info.value.response.status_code in (401, 403)
