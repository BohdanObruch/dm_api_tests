from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class CommentEnvelope(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    resource: Comment | None = None
    metadata: dict | None = None


class GeneralError(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    message: str | None = None


class Comment(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str | None = Field(default=None, alias="id")
    author: User | None = Field(default=None, alias="author")
    created: datetime | None = Field(default=None, alias="created")
    updated: datetime | None = Field(default=None, alias="updated")
    text: CommonBbText | str | None = Field(default=None, alias="text")
    likes: list[User] | None = Field(default=None, alias="likes")


class BadRequestError(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    message: str | None = None
    invalid_properties: dict | None = Field(default=None, alias="invalidProperties")


class UserEnvelope(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    resource: User | None = None
    metadata: dict | None = None


class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    login: str | None = Field(default=None, alias="login")
    roles: list[UserRole] | None = Field(default=None, alias="roles")
    medium_picture_url: str | None = Field(default=None, alias="mediumPictureUrl")
    small_picture_url: str | None = Field(default=None, alias="smallPictureUrl")
    status: str | None = Field(default=None, alias="status")
    rating: Rating | None = Field(default=None, alias="rating")
    online: datetime | None = Field(default=None, alias="online")
    name: str | None = Field(default=None, alias="name")
    location: str | None = Field(default=None, alias="location")
    registration: datetime | None = Field(default=None, alias="registration")


class CommonBbText(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    value: str | None = Field(default=None, alias="value")
    parse_mode: BbParseMode | None = Field(default=None, alias="parseMode")


class UserRole(StrEnum):
    Guest = "Guest"
    Player = "Player"
    Administrator = "Administrator"
    NannyModerator = "NannyModerator"
    RegularModerator = "RegularModerator"
    SeniorModerator = "SeniorModerator"


class Rating(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    enabled: bool | None = Field(default=None, alias="enabled")
    quality: int | None = Field(default=None, alias="quality")
    quantity: int | None = Field(default=None, alias="quantity")


class BbParseMode(StrEnum):
    Common = "Common"
    Info = "Info"
    Post = "Post"
    Chat = "Chat"


CommentEnvelope.model_rebuild()
Comment.model_rebuild()
BadRequestError.model_rebuild()
UserEnvelope.model_rebuild()
User.model_rebuild()
CommonBbText.model_rebuild()
Rating.model_rebuild()

