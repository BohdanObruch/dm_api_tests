from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class Paging(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    pages: int | None = Field(default=None, description="Total pages count", json_schema_extra={"read_only": True})
    current: int | None = Field(default=None, description="Current page number", json_schema_extra={"read_only": True})
    size: int | None = Field(default=None, description="Page size", json_schema_extra={"read_only": True})
    number: int | None = Field(default=None, description="Entity number", json_schema_extra={"read_only": True})
    total: int | None = Field(default=None, description="Total entity count", json_schema_extra={"read_only": True})


class UserRole(str, Enum):
    Guest = "Guest"
    Player = "Player"
    Administrator = "Administrator"
    NannyModerator = "NannyModerator"
    RegularModerator = "RegularModerator"
    SeniorModerator = "SeniorModerator"


class Rating(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    enabled: bool | None = Field(default=None, description="Rating participation flag")
    quality: int | None = Field(default=None, description="Quality rating")
    quantity: int | None = Field(default=None, description="Quantity rating")


class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    login: str | None = Field(default=None, description="Login")
    roles: list[UserRole] | None = Field(default=None, description="Roles")
    medium_picture_url: str | None = Field(default=None, alias="mediumPictureUrl", description="Profile picture URL M-size")
    small_picture_url: str | None = Field(default=None, alias="smallPictureUrl", description="Profile picture URL S-size")
    status: str | None = Field(default=None, description="User defined status")
    rating: Rating | None = None
    online: datetime | None = Field(default=None, description="Last seen online moment", json_schema_extra={"format": "date-time"})
    name: str | None = Field(default=None, description="User real name")
    location: str | None = Field(default=None, description="User real location")
    registration: datetime | None = Field(default=None, description="User registration moment", json_schema_extra={"format": "date-time"})


class BbParseMode(str, Enum):
    Common = "Common"
    Info = "Info"
    Post = "Post"
    Chat = "Chat"


class CommonBbText(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    value: str | None = Field(default=None, description="Text")
    parse_mode: BbParseMode | None = Field(default=None, alias="parseMode")


class Comment(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str | None = Field(default=None, description="Commentary identifier", json_schema_extra={"format": "uuid"})
    author: User | None = None
    created: datetime | None = Field(default=None, description="Creation moment", json_schema_extra={"format": "date-time"})
    updated: datetime | None = Field(default=None, description="Last update moment", json_schema_extra={"format": "date-time"})
    text: CommonBbText | None = None
    likes: list[User] | None = Field(default=None, description="Users who liked it")


class CommentEnvelope(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    resource: Comment | None = None
    metadata: dict | None = Field(default=None, description="Additional metadata")


class CommentListEnvelope(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    resources: list[Comment] | None = Field(default=None, description="Enveloped resources")
    paging: Paging | None = None


class GeneralError(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    message: str | None = Field(default=None, description="Client message")


class BadRequestError(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    message: str | None = Field(default=None, description="Client message")
    invalid_properties: dict[str, list[str]] | None = Field(default=None, alias="invalidProperties", description="Key-value pairs of invalid request properties")


class UserEnvelope(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    resource: User | None = None
    metadata: dict | None = Field(default=None, description="Additional metadata")
