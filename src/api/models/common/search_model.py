from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class Paging(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    pages: int | None = Field(default=None, description="Total pages count")
    current: int | None = Field(default=None, description="Current page number")
    size: int | None = Field(default=None, description="Page size")
    number: int | None = Field(default=None, description="Entity number")
    total: int | None = Field(default=None, description="Total entity count")


class ObjectListEnvelope(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    resources: list[dict] | None = Field(default=None, description="Enveloped resources")
    paging: Paging | None = None
