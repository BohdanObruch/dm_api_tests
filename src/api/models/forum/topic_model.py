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


class Rating(BaseModel):
    model_config = ConfigDict(extra="allow")

    enabled: bool | None = None
    quality: int | None = None
    quantity: int | None = None


class Paging(BaseModel):
    model_config = ConfigDict(extra="allow")

    pages: int | None = None
    current: int | None = None
    size: int | None = None
    number: int | None = None
    total: int | None = None


class User(BaseModel):
    model_config = ConfigDict(extra="allow")

    login: str | None = None
    roles: list[UserRole] | None = None
    rating: Rating | None = None


class CommonBbText(BaseModel):
    model_config = ConfigDict(extra="allow")

    value: str | None = None
    parse_mode: BbParseMode | None = Field(default=None, alias="parseMode")


class LastTopicComment(BaseModel):
    model_config = ConfigDict(extra="allow")

    created: datetime | None = None
    author: User | None = None


class Forum(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    unread_topics_count: int | None = Field(default=None, alias="unreadTopicsCount")


class Topic(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    author: User | None = None
    created: datetime | None = None
    title: str | None = None
    description: CommonBbText | str | None = None
    attached: bool | None = None
    closed: bool | None = None
    last_comment: LastTopicComment | None = Field(default=None, alias="lastComment")
    comments_count: int | None = Field(default=None, alias="commentsCount")
    unread_comments_count: int | None = Field(default=None, alias="unreadCommentsCount")
    forum: Forum | None = None
    likes: list[User] | None = None


class Comment(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    author: User | None = None
    created: datetime | None = None
    updated: datetime | None = None
    text: CommonBbText | str | None = None
    likes: list[User] | None = None


class TopicEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow")

    resource: Topic | None = None
    metadata: dict | None = None


class UserEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow")

    resource: User | None = None
    metadata: dict | None = None


class CommentEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow")

    resource: Comment | None = None
    metadata: dict | None = None


class CommentListEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow")

    resources: list[Comment] | None = None
    paging: Paging | None = None


class GeneralError(BaseModel):
    model_config = ConfigDict(extra="allow")

    message: str | None = None


class BadRequestError(BaseModel):
    model_config = ConfigDict(extra="allow")

    message: str | None = None
    invalid_properties: dict | None = Field(default=None, alias="invalidProperties")
