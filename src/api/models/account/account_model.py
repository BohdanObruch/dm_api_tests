from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Registration(BaseModel):
    login: str | None = Field(default=None)
    email: str | None = Field(default=None)
    password: str | None = Field(default=None)


class BadRequestError(BaseModel):
    message: str | None = Field(default=None, alias="message")
    invalid_properties: dict[str, list[str]] | None = Field(
        default=None, alias="invalidProperties"
    )


class UserDetailsEnvelope(BaseModel):
    resource: UserDetails | None = Field(default=None)
    metadata: dict | None = Field(default=None)


class UserEnvelope(BaseModel):
    resource: User | None = Field(default=None)
    metadata: dict | None = Field(default=None)


class GeneralError(BaseModel):
    message: str | None = Field(default=None, alias="message")


class ResetPassword(BaseModel):
    login: str | None = Field(default=None)
    email: str | None = Field(default=None)


class ChangePassword(BaseModel):
    login: str | None = Field(default=None)
    token: str | None = Field(default=None, json_schema_extra={"format": "uuid"})
    old_password: str | None = Field(default=None, alias="oldPassword")
    new_password: str | None = Field(default=None, alias="newPassword")


class ChangeEmail(BaseModel):
    login: str | None = Field(default=None)
    password: str | None = Field(default=None)
    email: str | None = Field(default=None)


class UserDetails(BaseModel):
    login: str | None = Field(default=None)
    roles: list[UserRole] | None = Field(default=None)
    medium_picture_url: str | None = Field(default=None, alias="mediumPictureUrl")
    small_picture_url: str | None = Field(default=None, alias="smallPictureUrl")
    status: str | None = Field(default=None)
    rating: Rating = Field(alias="rating")
    online: datetime | None = Field(default=None, json_schema_extra={"format": "date-time"})
    name: str | None = Field(default=None)
    location: str | None = Field(default=None)
    registration: datetime | None = Field(default=None, json_schema_extra={"format": "date-time"})
    icq: str | None = Field(default=None)
    skype: str | None = Field(default=None)
    original_picture_url: str | None = Field(default=None, alias="originalPictureUrl")
    info: InfoBbText | str | None = Field(default=None, alias="info")
    settings: UserSettings | dict[str, Any] | None = Field(default=None, alias="settings")


class User(BaseModel):
    login: str | None = Field(default=None)
    token: str | None = Field(default=None, json_schema_extra={"format": "uuid"})
    email: str | None = Field(default=None)
    roles: list[UserRole] | None = Field(default=None)
    medium_picture_url: str | None = Field(default=None, alias="mediumPictureUrl")
    small_picture_url: str | None = Field(default=None, alias="smallPictureUrl")
    status: str | None = Field(default=None)
    rating: Rating = Field(alias="rating")
    online: datetime | None = Field(default=None, json_schema_extra={"format": "date-time"})
    name: str | None = Field(default=None)
    location: str | None = Field(default=None)
    registration: datetime | None = Field(default=None, json_schema_extra={"format": "date-time"})


class UserRole(str, Enum):
    Guest = "Guest"
    Player = "Player"
    Administrator = "Administrator"
    NannyModerator = "NannyModerator"
    RegularModerator = "RegularModerator"
    SeniorModerator = "SeniorModerator"


class Rating(BaseModel):
    enabled: bool | None = Field(default=None)
    quality: int | None = Field(default=None, json_schema_extra={"format": "int32"})
    quantity: int | None = Field(default=None, json_schema_extra={"format": "int32"})


class InfoBbText(BaseModel):
    value: str | None = Field(default=None)
    parse_mode: BbParseMode = Field(alias="parseMode")


class UserSettings(BaseModel):
    color_schema: ColorSchema = Field(alias="colorSchema")
    nanny_greetings_message: str | None = Field(default=None, alias="nannyGreetingsMessage")
    paging: PagingSettings = Field(alias="paging")


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


class PagingSettings(BaseModel):
    posts_per_page: int | None = Field(default=None, alias="postsPerPage", json_schema_extra={"format": "int32"})
    comments_per_page: int | None = Field(
        default=None, alias="commentsPerPage", json_schema_extra={"format": "int32"}
    )
    topics_per_page: int | None = Field(default=None, alias="topicsPerPage", json_schema_extra={"format": "int32"})
    messages_per_page: int | None = Field(
        default=None, alias="messagesPerPage", json_schema_extra={"format": "int32"}
    )
    entities_per_page: int | None = Field(
        default=None, alias="entitiesPerPage", json_schema_extra={"format": "int32"}
    )
