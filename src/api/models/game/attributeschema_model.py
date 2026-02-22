from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class Paging(BaseModel):
    model_config = ConfigDict(extra="allow")

    pages: int | None = None
    current: int | None = None
    size: int | None = None
    number: int | None = None
    total: int | None = None


class SchemaType(str, Enum):
    Public = "Public"
    Private = "Private"


class AttributeSpecificationType(str, Enum):
    Number = "Number"
    String = "String"
    List = "List"


class UserRole(str, Enum):
    Guest = "Guest"
    Player = "Player"
    Administrator = "Administrator"
    NannyModerator = "NannyModerator"
    RegularModerator = "RegularModerator"
    SeniorModerator = "SeniorModerator"


class AttributeValueSpecification(BaseModel):
    model_config = ConfigDict(extra="allow")

    value: str | None = None
    modifier: int | None = None


class Rating(BaseModel):
    model_config = ConfigDict(extra="allow")

    enabled: bool | None = None
    quality: int | None = None
    quantity: int | None = None


class User(BaseModel):
    model_config = ConfigDict(extra="allow")

    login: str | None = None
    roles: list[UserRole] | None = None
    medium_picture_url: str | None = Field(default=None, alias="mediumPictureUrl")
    small_picture_url: str | None = Field(default=None, alias="smallPictureUrl")
    status: str | None = None
    rating: Rating | None = None
    online: datetime | None = None
    name: str | None = None
    location: str | None = None
    registration: datetime | None = None


class AttributeSpecification(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    title: str | None = None
    required: bool | None = None
    type: AttributeSpecificationType | None = None
    min_value: int | None = Field(default=None, alias="minValue")
    max_value: int | None = Field(default=None, alias="maxValue")
    max_length: int | None = Field(default=None, alias="maxLength")
    values: list[AttributeValueSpecification] | None = None


class AttributeSchema(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    title: str | None = None
    author: User | None = None
    type: SchemaType | None = None
    specifications: list[AttributeSpecification] | None = None


class AttributeSchemaListEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow")

    resources: list[AttributeSchema] | None = None
    paging: Paging | None = None


class AttributeSchemaEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow")

    resource: AttributeSchema | None = None
    metadata: dict | None = None


class BadRequestError(BaseModel):
    model_config = ConfigDict(extra="allow")

    message: str | None = None
    invalid_properties: dict[str, list[str]] | None = Field(default=None, alias="invalidProperties")


class GeneralError(BaseModel):
    model_config = ConfigDict(extra="allow")

    message: str | None = None
