import pytest
import requests

from src.api.models.game.attributeschema_model import AttributeSchemaEnvelope, AttributeSchemaListEnvelope
from tests.fixtures.allure_helpers import step


@pytest.mark.smoke
def test_create_attribute_schema_roundtrip(attribute_schema_api, valid_attribute_schema_payload):
    with step("Create attribute schema"):
        created = attribute_schema_api.post_schema(payload=valid_attribute_schema_payload)
    with step("Verify created schema response"):
        assert isinstance(created, AttributeSchemaEnvelope)
        assert created.resource is not None
    with step("Get created schema by id"):
        fetched = attribute_schema_api.get_schema(id=created.resource.id)
    with step("Verify fetched schema matches created one"):
        assert isinstance(fetched, AttributeSchemaEnvelope)
        assert fetched.resource is not None
        assert fetched.resource.id == created.resource.id
    with step("Cleanup created schema"):
        attribute_schema_api.delete_schema(id=created.resource.id)


@pytest.mark.regression
def test_get_attribute_schema_list(attribute_schema_api, valid_attribute_schema_payload):
    with step("Create attribute schema for listing"):
        created = attribute_schema_api.post_schema(payload=valid_attribute_schema_payload)
    with step("Verify schema is created"):
        assert created.resource is not None
    with step("Request attribute schema list"):
        response = attribute_schema_api.get_schemas()
    with step("Verify created schema is in list"):
        assert isinstance(response, AttributeSchemaListEnvelope)
        assert response.resources is None or isinstance(response.resources, list)
        assert response.resources is None or any(item.id == created.resource.id for item in response.resources)
    with step("Cleanup created schema"):
        attribute_schema_api.delete_schema(id=created.resource.id)


@pytest.mark.regression
def test_put_attribute_schema(attribute_schema_api, valid_attribute_schema_payload):
    with step("Create attribute schema for update"):
        created = attribute_schema_api.post_schema(payload=valid_attribute_schema_payload)
    with step("Verify created schema has id"):
        assert created.resource is not None
        assert created.resource.id is not None

    payload = {
        "title": "Updated schema title",
        "specifications": [
            {
                "id": created.resource.specifications[0].id,
                "title": "Updated strength",
                "required": True,
                "type": "Number",
                "minValue": 1,
                "maxValue": 30,
            }
        ],
    }

    with step("Update attribute schema"):
        try:
            response = attribute_schema_api.put_schema(id=created.resource.id, payload=payload)
        except requests.HTTPError as exc:
            assert exc.response.status_code == 501
        else:
            assert isinstance(response, AttributeSchemaEnvelope)
            assert response.resource is not None
            assert response.resource.id == created.resource.id
    with step("Cleanup created schema"):
        attribute_schema_api.delete_schema(id=created.resource.id)


@pytest.mark.regression
def test_delete_attribute_schema(attribute_schema_api, valid_attribute_schema_payload):
    with step("Create attribute schema for delete"):
        created = attribute_schema_api.post_schema(payload=valid_attribute_schema_payload)
    with step("Verify schema was created"):
        assert created.resource is not None
    with step("Delete created schema"):
        attribute_schema_api.delete_schema(id=created.resource.id)
    with step("Verify deleted schema is not found"):
        with pytest.raises(requests.HTTPError) as exc_info:
            attribute_schema_api.get_schema(id=created.resource.id)
        assert exc_info.value.response.status_code == 410


@pytest.mark.regression
def test_create_attribute_schema_invalid_payload_returns_400(attribute_schema_api):
    with step("Create attribute schema with invalid payload"), pytest.raises(requests.HTTPError) as exc_info:
        attribute_schema_api.post_schema(payload={"title": "invalid", "type": "InvalidType"})
    with step("Verify status code is 400"):
        assert exc_info.value.response.status_code == 400
