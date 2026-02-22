from __future__ import annotations

from src.api.controllers.base_controller import BaseController
from src.api.models.game.attributeschema_model import (
    AttributeSchemaEnvelope,
    AttributeSchemaListEnvelope,
)


class AttributeSchemaController(BaseController):
    def get_schemas(self) -> AttributeSchemaListEnvelope:
        data = self._get("/v1/schemata")
        return AttributeSchemaListEnvelope.model_validate(data)

    def post_schema(self, payload: dict) -> AttributeSchemaEnvelope:
        data = self._post("/v1/schemata", data=payload)
        return AttributeSchemaEnvelope.model_validate(data)

    def get_schema(self, id: str) -> AttributeSchemaEnvelope:
        data = self._get(f"/v1/schemata/{id}")
        return AttributeSchemaEnvelope.model_validate(data)

    def put_schema(self, id: str, payload: dict) -> AttributeSchemaEnvelope:
        data = self._patch(f"/v1/schemata/{id}", data=payload)
        return AttributeSchemaEnvelope.model_validate(data)

    def delete_schema(self, id: str) -> dict | None:
        return self._delete(f"/v1/schemata/{id}")
