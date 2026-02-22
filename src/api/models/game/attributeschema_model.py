from __future__ import annotations

from src.api.models.game.common_model import (
    AttributeSchema,
    AttributeSpecification,
    AttributeSpecificationType,
    AttributeValueSpecification,
    BadRequestError,
    GeneralError,
    SchemaType,
    User,
)
from src.api.models.shared.base_model import ResourceEnvelope, ResourceListEnvelope

AttributeSchemaListEnvelope = ResourceListEnvelope[AttributeSchema]
AttributeSchemaEnvelope = ResourceEnvelope[AttributeSchema]


__all__ = [
    "AttributeSchema",
    "AttributeSchemaEnvelope",
    "AttributeSchemaListEnvelope",
    "AttributeSpecification",
    "AttributeSpecificationType",
    "AttributeValueSpecification",
    "BadRequestError",
    "GeneralError",
    "SchemaType",
    "User",
]
