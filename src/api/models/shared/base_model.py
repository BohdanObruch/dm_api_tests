from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class Paging(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    pages: int | None = None
    current: int | None = None
    size: int | None = None
    number: int | None = None
    total: int | None = None


class ApiIgnoreModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class ResourceEnvelope[T](BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    resource: T | None = None
    metadata: dict | None = None


class ResourceListEnvelope[T](BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    resources: list[T] | None = None
    paging: Paging | None = None


class GeneralError(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    message: str | None = None


class BadRequestError(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    message: str | None = None
    invalid_properties: dict[str, list[str]] | None = Field(default=None, alias="invalidProperties")
