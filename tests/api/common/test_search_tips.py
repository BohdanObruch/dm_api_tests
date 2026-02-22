import pytest
import requests
from faker import Faker

from src.api.controllers.common.search_controller import SearchApi
from src.api.models.common.search_model import ObjectListEnvelope, Paging
from tests.fixtures.allure_helpers import step

pytestmark = [pytest.mark.api]

fake = Faker()


@pytest.mark.smoke
def test_search_roundtrip(search_api):
    with step("Generate random search query"):
        query_term = fake.word()

    with step(f"Send search request with query='{query_term}' and size=5"):
        result: ObjectListEnvelope = search_api.search(query=query_term, size=5)

    with step("Verify response envelope type"):
        assert isinstance(result, ObjectListEnvelope)
    with step("Verify paging section type"):
        assert isinstance(result.paging, Paging)
    with step("Verify resources is a list"):
        assert isinstance(result.resources, list)


@pytest.mark.regression
def test_search_with_pagination(search_api):
    with step("Prepare pagination values"):
        query_term = fake.word()
        skip_value = 10
        size_value = 3

    with step(f"Send search request with query='{query_term}', skip={skip_value}, size={size_value}"):
        result: ObjectListEnvelope = search_api.search(query=query_term, skip=skip_value, size=size_value)

    with step("Verify response envelope type"):
        assert isinstance(result, ObjectListEnvelope)
    with step("Verify paging section type"):
        assert isinstance(result.paging, Paging)
    with step(f"Verify page size is: {size_value}"):
        assert result.paging.size == size_value
    with step(f"Verify resources count is <= {size_value}"):
        assert len(result.resources) <= size_value


@pytest.mark.regression
def test_search_empty_result(search_api):
    with step("Use unlikely query for empty result case"):
        query_term = "a_very_unlikely_and_specific_search_term_xyz12345"

    with step(f"Send search request with query='{query_term}'"):
        result: ObjectListEnvelope = search_api.search(query=query_term)

    with step("Verify response envelope type"):
        assert isinstance(result, ObjectListEnvelope)
    with step("Verify resources list is empty"):
        assert result.resources == []
    with step("Verify paging section is present"):
        assert result.paging is not None
    with step("Verify total found items is 0"):
        assert result.paging.total == 0


@pytest.mark.regression
def test_search_invalid_query_handling(search_api):
    with step("Send invalid search request with empty query"), pytest.raises(requests.exceptions.HTTPError) as exc_info:
        search_api.search(query="")

    with step("Verify response status code is expected for invalid query"):
        assert exc_info.value.response.status_code in (400, 500)


@pytest.mark.regression
def test_search_without_token_returns_valid_response_or_auth_error(configs):
    api = SearchApi(base_url=configs.app_base_url)
    with step("Call search without token"):
        try:
            result = api.search(query=fake.word(), size=3)
        except requests.HTTPError as exc_info:
            assert exc_info.response.status_code in (401, 403)
            return
    with step("If endpoint is public, verify normal response structure"):
        assert isinstance(result, ObjectListEnvelope)
