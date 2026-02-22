from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class Paging(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    pages: int | None = Field(default=None, description="Total pages count", json_schema_extra={"read_only": True})
    current: int | None = Field(default=None, description="Current page number", json_schema_extra={"read_only": True})
    size: int | None = Field(default=None, description="Page size", json_schema_extra={"read_only": True})
    number: int | None = Field(default=None, description="Entity number", json_schema_extra={"read_only": True})
    total: int | None = Field(default=None, description="Total entity count", json_schema_extra={"read_only": True})


class GeneralError(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    message: str | None = Field(default=None, description="Client message")


class BadRequestError(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    message: str | None = Field(default=None, description="Client message")
    invalid_properties: dict[str, list[str]] | None = Field(
        default=None, alias="invalidProperties", description="Key-value pairs of invalid request properties"
    )


class BbParseMode(StrEnum):
    COMMON = "Common"
    INFO = "Info"
    POST = "Post"
    CHAT = "Chat"


class CommonBbText(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    value: str | None = Field(default=None, description="Text")
    parse_mode: BbParseMode = Field(alias="parseMode")


class UserRole(StrEnum):
    GUEST = "Guest"
    PLAYER = "Player"
    ADMINISTRATOR = "Administrator"
    NannyModerator = "NannyModerator"
    RegularModerator = "RegularModerator"
    SeniorModerator = "SeniorModerator"


class Rating(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    enabled: bool = Field(description="Rating participation flag")
    quality: int = Field(description="Quality rating", json_schema_extra={"format": "int32"})
    quantity: int = Field(description="Quantity rating", json_schema_extra={"format": "int32"})


class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    login: str | None = Field(default=None, description="Login")
    roles: list[UserRole] | None = Field(default=None, description="Roles")
    medium_picture_url: str | None = Field(
        default=None, alias="mediumPictureUrl", description="Profile picture URL M-size"
    )
    small_picture_url: str | None = Field(
        default=None, alias="smallPictureUrl", description="Profile picture URL S-size"
    )
    status: str | None = Field(default=None, description="User defined status")
    rating: Rating | None = Field(default=None)
    online: datetime | None = Field(default=None, description="Last seen online moment", json_schema_extra={"format": "date-time"})
    name: str | None = Field(default=None, description="User real name")
    location: str | None = Field(default=None, description="User real location")
    registration: datetime | None = Field(default=None, description="User registration moment", json_schema_extra={"format": "date-time"})


class Message(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str = Field(description="Identifier", json_schema_extra={"format": "uuid"})
    created: datetime = Field(description="Creating moment", json_schema_extra={"format": "date-time"})
    author: User = Field()
    text: CommonBbText = Field()


class Conversation(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str = Field(description="Identifier", json_schema_extra={"format": "uuid"})
    name: str | None = Field(default=None, description="Conversation name")
    participants: list[User] | None = Field(default=None, description="Conversation participants")
    last_message: Message | None = Field(default=None, alias="lastMessage")
    unread_messages_count: int = Field(
        description="Number of unread conversation messages",
        json_schema_extra={"format": "int32"},
    )


class ConversationEnvelope(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    resource: Conversation | None = None
    metadata: dict | None = Field(default=None, description="Additional metadata")


class ConversationListEnvelope(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    resources: list[Conversation] | None = Field(default=None, description="Enveloped resources")
    paging: Paging | None = Field(default=None)


class MessageEnvelope(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    resource: Message | None = None
    metadata: dict | None = Field(default=None, description="Additional metadata")


class MessageListEnvelope(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    resources: list[Message] | None = Field(default=None, description="Enveloped resources")
    paging: Paging | None = Field(default=None)
