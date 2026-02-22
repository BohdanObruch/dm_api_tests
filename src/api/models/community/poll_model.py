from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PollListEnvelope(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    resources: list[Poll] | None = Field(default=None, alias="resources")
    paging: Paging | None = Field(default=None, alias="paging")


class Poll(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str | None = Field(default=None, alias="id")
    ends: datetime | None = Field(default=None, alias="ends")
    title: str | None = Field(default=None, alias="title")
    options: list[PollOption] | None = Field(default=None, alias="options")


class PollEnvelope(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    resource: Poll | None = Field(default=None, alias="resource")
    metadata: dict | None = Field(default=None, alias="metadata")


class BadRequestError(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    message: str | None = Field(default=None, alias="message")
    invalid_properties: dict | None = Field(default=None, alias="invalidProperties")


class GeneralError(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    message: str | None = Field(default=None, alias="message")


class Paging(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    pages: int | None = Field(default=None, alias="pages")
    current: int | None = Field(default=None, alias="current")
    size: int | None = Field(default=None, alias="size")
    number: int | None = Field(default=None, alias="number")
    total: int | None = Field(default=None, alias="total")


class PollOption(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str | None = Field(default=None, alias="id")
    text: str | None = Field(default=None, alias="text")
    votes_count: int | None = Field(default=None, alias="votesCount")
    voted: bool | None = Field(default=None, alias="voted")
