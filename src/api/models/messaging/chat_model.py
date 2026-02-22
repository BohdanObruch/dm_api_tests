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
    medium_picture_url: str | None = Field(default=None, alias="mediumPictureUrl")
    small_picture_url: str | None = Field(default=None, alias="smallPictureUrl")
    status: str | None = None
    rating: Rating | None = None
    online: datetime | None = None
    name: str | None = None
    location: str | None = None
    registration: datetime | None = None


class ChatBbText(BaseModel):
    model_config = ConfigDict(extra="allow")

    value: str | None = None
    parse_mode: BbParseMode | None = Field(default=None, alias="parseMode")


class ChatMessage(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    created: datetime | None = None
    author: User | None = None
    text: ChatBbText | None = None


class ChatMessageEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow")

    resource: ChatMessage | None = None
    metadata: dict | None = None


class ChatMessageListEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow")

    resources: list[ChatMessage] | None = None
    paging: Paging | None = None
