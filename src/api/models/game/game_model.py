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


class GameStatus(str, Enum):
    Closed = "Closed"
    Finished = "Finished"
    Frozen = "Frozen"
    Requirement = "Requirement"
    Draft = "Draft"
    Active = "Active"
    RequiresModeration = "RequiresModeration"
    Moderation = "Moderation"


class BbParseMode(str, Enum):
    Common = "Common"
    Info = "Info"
    Post = "Post"
    Chat = "Chat"


class CommentariesAccessMode(str, Enum):
    Public = "Public"
    Readonly = "Readonly"
    Private = "Private"


class SchemaType(str, Enum):
    Public = "Public"
    Private = "Private"


class GameParticipation(str, Enum):
    NONE = "None"
    Reader = "Reader"
    Player = "Player"
    Moderator = "Moderator"
    PendingAssistant = "PendingAssistant"
    Authority = "Authority"
    Owner = "Owner"


class AttributeSpecificationType(str, Enum):
    Number = "Number"
    String = "String"
    List = "List"


class AttributeValueSpecification(BaseModel):
    model_config = ConfigDict(extra="allow")

    value: str | None = None
    modifier: int | None = None


class AttributeSpecification(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    title: str | None = None
    required: bool | None = None
    type: AttributeSpecificationType | None = None
    minValue: int | None = None
    maxValue: int | None = None
    maxLength: int | None = None
    values: list[AttributeValueSpecification] | None = None


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


class InfoBbText(BaseModel):
    model_config = ConfigDict(extra="allow")

    value: str | None = None
    parseMode: BbParseMode | None = None


class GamePrivacySettings(BaseModel):
    model_config = ConfigDict(extra="allow")

    viewTemper: bool | None = None
    viewStory: bool | None = None
    viewSkills: bool | None = None
    viewInventory: bool | None = None
    viewPrivates: bool | None = None
    viewDice: bool | None = None
    commentariesAccess: CommentariesAccessMode | None = None


class AttributeSchema(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    title: str | None = None
    author: User | None = None
    type: SchemaType | None = None
    specifications: list[AttributeSpecification] | None = None


class Tag(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    title: str | None = None
    category: str | None = None


class Game(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    title: str | None = None
    system: str | None = None
    setting: str | None = None
    schema_: AttributeSchema | None = Field(default=None, alias="schema")
    status: GameStatus | None = None
    released: datetime | None = None
    master: User | None = None
    assistant: User | None = None
    nanny: User | None = None
    pendingAssistant: User | None = None
    participation: list[GameParticipation] | None = None
    tags: list[Tag] | None = None
    info: InfoBbText | None = None
    notes: str | None = None
    privacySettings: GamePrivacySettings | None = None
    unreadPostsCount: int | None = None
    unreadCommentsCount: int | None = None
    unreadCharactersCount: int | None = None


class GameListEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow")

    resources: list[Game] | None = None
    paging: Paging | None = None


class GameEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow")

    resource: Game | None = None
    metadata: dict | None = None


class TagListEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow")

    resources: list[Tag] | None = None
    paging: Paging | None = None


class UserListEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow")

    resources: list[User] | None = None
    paging: Paging | None = None


class UserEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow")

    resource: User | None = None
    metadata: dict | None = None


class BadRequestError(BaseModel):
    model_config = ConfigDict(extra="allow")

    message: str | None = None
    invalidProperties: dict[str, list[str]] | None = None


class GeneralError(BaseModel):
    model_config = ConfigDict(extra="allow")

    message: str | None = None
