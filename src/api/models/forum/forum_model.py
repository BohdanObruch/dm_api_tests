from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class UserRole(StrEnum):
    Guest = "Guest"
    Player = "Player"
    Administrator = "Administrator"
    NannyModerator = "NannyModerator"
    RegularModerator = "RegularModerator"
    SeniorModerator = "SeniorModerator"


class BbParseMode(StrEnum):
    Common = "Common"
    Info = "Info"
    Post = "Post"
    Chat = "Chat"


class Rating(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    enabled: bool | None = Field(default=None, alias="enabled")
    quality: int | None = Field(default=None, alias="quality")
    quantity: int | None = Field(default=None, alias="quantity")


class Paging(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    pages: int | None = Field(default=None, alias="pages")
    current: int | None = Field(default=None, alias="current")
    size: int | None = Field(default=None, alias="size")
    number: int | None = Field(default=None, alias="number")
    total: int | None = Field(default=None, alias="total")


class CommonBbText(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    value: str | None = Field(default=None, alias="value")
    parse_mode: BbParseMode | None = Field(default=None, alias="parseMode")


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


class Forum(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str | None = Field(default=None, alias="id")
    unread_topics_count: int | None = Field(default=None, alias="unreadTopicsCount")


class LastTopicComment(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    created: datetime | None = Field(default=None, alias="created")
    author: User | None = Field(default=None, alias="author")


class Topic(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str | None = Field(default=None, alias="id")
    author: User | None = Field(default=None, alias="author")
    created: datetime | None = Field(default=None, alias="created")
    title: str | None = Field(default=None, alias="title")
    description: CommonBbText | str | None = Field(default=None, alias="description")
    attached: bool | None = Field(default=None, alias="attached")
    closed: bool | None = Field(default=None, alias="closed")
    last_comment: LastTopicComment | None = Field(default=None, alias="lastComment")
    comments_count: int | None = Field(default=None, alias="commentsCount")
    unread_comments_count: int | None = Field(default=None, alias="unreadCommentsCount")
    forum: Forum | None = Field(default=None, alias="forum")
    likes: list[User] | None = Field(default=None, alias="likes")


class ForumListEnvelope(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    resources: list[Forum] | None = Field(default=None, alias="resources")
    paging: Paging | None = Field(default=None, alias="paging")


class ForumEnvelope(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    resource: Forum | None = Field(default=None, alias="resource")
    metadata: dict | None = Field(default=None, alias="metadata")


class UserListEnvelope(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    resources: list[User] | None = Field(default=None, alias="resources")
    paging: Paging | None = Field(default=None, alias="paging")


class TopicListEnvelope(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    resources: list[Topic] | None = Field(default=None, alias="resources")
    paging: Paging | None = Field(default=None, alias="paging")


class TopicEnvelope(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    resource: Topic | None = Field(default=None, alias="resource")
    metadata: dict | None = Field(default=None, alias="metadata")


class GeneralError(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    message: str | None = Field(default=None, alias="message")


class BadRequestError(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    message: str | None = Field(default=None, alias="message")
    invalid_properties: dict[str, list[str]] | None = Field(default=None, alias="invalidProperties")
