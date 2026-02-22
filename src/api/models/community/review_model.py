from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class Paging(BaseModel):
    model_config = ConfigDict(extra="allow")

    pages: int | None = None
    current: int | None = None
    size: int | None = None
    number: int | None = None
    total: int | None = None


class UserRole(str, Enum):
    Guest = "Guest"
    Player = "Player"
    Administrator = "Administrator"
    NannyModerator = "NannyModerator"
    RegularModerator = "RegularModerator"
    SeniorModerator = "SeniorModerator"


class BbParseMode(str, Enum):
    Common = "Common"
    Info = "Info"
    Post = "Post"
    Chat = "Chat"


class Rating(BaseModel):
    model_config = ConfigDict(extra="allow")

    enabled: bool | None = None
    quality: int | None = None
    quantity: int | None = None


class User(BaseModel):
    model_config = ConfigDict(extra="allow")

    login: str | None = None
    roles: list[UserRole] | None = None
    rating: Rating | None = None


class CommonBbText(BaseModel):
    model_config = ConfigDict(extra="allow")

    value: str | None = None
    parseMode: BbParseMode | None = None


class Review(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    author: User | None = None
    created: datetime | None = None
    approved: bool | None = None
    text: CommonBbText | None = None


class ReviewListEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow")

    resources: list[Review] | None = None
    paging: Paging | None = None


class ReviewEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow")

    resource: Review | None = None
    metadata: dict | None = None


class GeneralError(BaseModel):
    model_config = ConfigDict(extra="allow")

    message: str | None = None


class BadRequestError(BaseModel):
    model_config = ConfigDict(extra="allow")

    message: str | None = None
    invalidProperties: dict[str, list[str]] | None = None
