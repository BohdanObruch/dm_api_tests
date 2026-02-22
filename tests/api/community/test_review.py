import pytest
import requests

from src.api.controllers.community.review_controller import ReviewApi
from src.api.models.community.review_model import ReviewListEnvelope
from tests.fixtures.allure_helpers import step

pytestmark = [pytest.mark.api]


@pytest.mark.smoke
def test_list_reviews(review_api):
    with step("Get reviews list"):
        review_list_envelope = review_api.list()
    with step("Verify reviews list response"):
        assert isinstance(review_list_envelope, ReviewListEnvelope)
        assert review_list_envelope.resources is None or isinstance(review_list_envelope.resources, list)


@pytest.mark.regression
def test_create_review_forbidden_for_regular_user(review_api, valid_review_payload: dict):
    with step("Create review as regular user"), pytest.raises(requests.HTTPError) as exc_info:
        review_api.create(payload=valid_review_payload)
    with step("Verify status code is 401 or 403"):
        assert exc_info.value.response.status_code in (401, 403)


@pytest.mark.regression
def test_create_review_invalid_payload_returns_400(review_api):
    with step("Create review with invalid payload"), pytest.raises(requests.HTTPError) as exc_info:
        review_api.create(payload={"text": {"value": "bad object"}, "approved": False})
    with step("Verify status code is 400"):
        assert exc_info.value.response.status_code == 400


@pytest.mark.regression
def test_get_review_by_invalid_id_returns_410(review_api):
    with step("Get review by invalid id"), pytest.raises(requests.HTTPError) as exc_info:
        review_api.get_by_id(id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 410"):
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_update_review_by_invalid_id_returns_400_or_410(review_api, valid_review_payload: dict):
    with step("Update review by invalid id"), pytest.raises(requests.HTTPError) as exc_info:
        review_api.update(id="00000000-0000-0000-0000-000000000000", payload=valid_review_payload)
    with step("Verify status code is 400, 401, or 410"):
        assert exc_info.value.response.status_code in (400, 401, 410)


@pytest.mark.regression
def test_delete_review_by_invalid_id_returns_410(review_api):
    with step("Delete review by invalid id"), pytest.raises(requests.HTTPError) as exc_info:
        review_api.delete(id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 401 or 410"):
        assert exc_info.value.response.status_code in (401, 410)


@pytest.mark.regression
def test_create_review_without_token_returns_401_or_403(configs, valid_review_payload: dict):
    api = ReviewApi(base_url=configs.app_base_url)
    with step("Create review without auth token"), pytest.raises(requests.HTTPError) as exc_info:
        api.create(payload=valid_review_payload)
    with step("Verify status code is 401 or 403"):
        assert exc_info.value.response.status_code in (401, 403)


@pytest.mark.regression
def test_update_review_without_token_returns_401_or_403(configs, valid_review_payload: dict):
    api = ReviewApi(base_url=configs.app_base_url)
    with step("Update review without auth token"), pytest.raises(requests.HTTPError) as exc_info:
        api.update(id="00000000-0000-0000-0000-000000000000", payload=valid_review_payload)
    with step("Verify status code is 401 or 403"):
        assert exc_info.value.response.status_code in (401, 403)


@pytest.mark.regression
def test_delete_review_without_token_returns_401_or_403(configs):
    api = ReviewApi(base_url=configs.app_base_url)
    with step("Delete review without auth token"), pytest.raises(requests.HTTPError) as exc_info:
        api.delete(id="00000000-0000-0000-0000-000000000000")
    with step("Verify status code is 401 or 403"):
        assert exc_info.value.response.status_code in (401, 403)
