from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


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


class ColorSchema(str, Enum):
    Modern = "Modern"
    Pale = "Pale"
    Classic = "Classic"
    ClassicPale = "ClassicPale"
    Night = "Night"


class Paging(BaseModel):
    model_config = ConfigDict(extra="allow")

    pages: int | None = None
    current: int | None = None
    size: int | None = None
    number: int | None = None
    total: int | None = None


class Rating(BaseModel):
    model_config = ConfigDict(extra="allow")

    enabled: bool | None = None
    quality: int | None = None
    quantity: int | None = None


class InfoBbText(BaseModel):
    model_config = ConfigDict(extra="allow")

    value: str | None = None
    parse_mode: BbParseMode | None = Field(default=None, alias="parseMode")


class PagingSettings(BaseModel):
    model_config = ConfigDict(extra="allow")

    posts_per_page: int | None = Field(default=None, alias="postsPerPage")
    comments_per_page: int | None = Field(default=None, alias="commentsPerPage")
    topics_per_page: int | None = Field(default=None, alias="topicsPerPage")
    messages_per_page: int | None = Field(default=None, alias="messagesPerPage")
    entities_per_page: int | None = Field(default=None, alias="entitiesPerPage")


class UserSettings(BaseModel):
    model_config = ConfigDict(extra="allow")

    color_schema: ColorSchema | None = Field(default=None, alias="colorSchema")
    nanny_greetings_message: str | None = Field(default=None, alias="nannyGreetingsMessage")
    paging: PagingSettings | None = None


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


class UserDetails(User):
    icq: str | None = None
    skype: str | None = None
    original_picture_url: str | None = Field(default=None, alias="originalPictureUrl")
    info: InfoBbText | str | None = None
    settings: UserSettings | None = None


class UserListEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow")

    resources: list[User] | None = None
    paging: Paging | None = None


class UserEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow")

    resource: User | None = None
    metadata: dict | None = None


class UserDetailsEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow")

    resource: UserDetails | None = None
    metadata: dict | None = None


class GeneralError(BaseModel):
    model_config = ConfigDict(extra="allow")

    message: str | None = None


class BadRequestError(BaseModel):
    model_config = ConfigDict(extra="allow")

    message: str | None = None
    invalid_properties: dict[str, list[str]] | None = Field(default=None, alias="invalidProperties")
