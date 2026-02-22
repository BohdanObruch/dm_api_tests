from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from src.api.models.game.common_model import (
    AttributeSchema,
    AttributeSpecificationType,
    AttributeValueSpecification,
    BadRequestError,
    BbParseMode,
    GeneralError,
    Paging,
    Rating,
    SchemaType,
    User,
)
from src.api.models.shared.base_model import ResourceEnvelope, ResourceListEnvelope


class GameStatus(str, Enum):
    Closed = "Closed"
    Finished = "Finished"
    Frozen = "Frozen"
    Requirement = "Requirement"
    Draft = "Draft"
    Active = "Active"
    RequiresModeration = "RequiresModeration"
    Moderation = "Moderation"


class CommentariesAccessMode(str, Enum):
    Public = "Public"
    Readonly = "Readonly"
    Private = "Private"


class GameParticipation(str, Enum):
    NONE = "None"
    Reader = "Reader"
    Player = "Player"
    Moderator = "Moderator"
    PendingAssistant = "PendingAssistant"
    Authority = "Authority"
    Owner = "Owner"


class InfoBbText(BaseModel):
    model_config = ConfigDict(extra="allow")

    value: str | None = None
    parse_mode: BbParseMode | None = Field(default=None, alias="parseMode")


class GamePrivacySettings(BaseModel):
    model_config = ConfigDict(extra="allow")

    view_temper: bool | None = Field(default=None, alias="viewTemper")
    view_story: bool | None = Field(default=None, alias="viewStory")
    view_skills: bool | None = Field(default=None, alias="viewSkills")
    view_inventory: bool | None = Field(default=None, alias="viewInventory")
    view_privates: bool | None = Field(default=None, alias="viewPrivates")
    view_dice: bool | None = Field(default=None, alias="viewDice")
    commentaries_access: CommentariesAccessMode | None = Field(default=None, alias="commentariesAccess")


class Tag(BaseModel):
    id: str | None = None
    title: str | None = None
    category: str | None = None


class Game(BaseModel):
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
    pending_assistant: User | None = Field(default=None, alias="pendingAssistant")
    participation: list[GameParticipation] | None = None
    tags: list[Tag] | None = None
    info: InfoBbText | None = None
    notes: str | None = None
    privacy_settings: GamePrivacySettings | None = Field(default=None, alias="privacySettings")
    unread_posts_count: int | None = Field(default=None, alias="unreadPostsCount")
    unread_comments_count: int | None = Field(default=None, alias="unreadCommentsCount")
    unread_characters_count: int | None = Field(default=None, alias="unreadCharactersCount")


GameListEnvelope = ResourceListEnvelope[Game]
GameEnvelope = ResourceEnvelope[Game]
TagListEnvelope = ResourceListEnvelope[Tag]
UserListEnvelope = ResourceListEnvelope[User]
UserEnvelope = ResourceEnvelope[User]


__all__ = [
    "AttributeSchema",
    "AttributeSpecificationType",
    "AttributeValueSpecification",
    "BadRequestError",
    "CommentariesAccessMode",
    "Game",
    "GameEnvelope",
    "GameListEnvelope",
    "GameParticipation",
    "GamePrivacySettings",
    "GameStatus",
    "GeneralError",
    "InfoBbText",
    "Paging",
    "Rating",
    "SchemaType",
    "Tag",
    "TagListEnvelope",
    "User",
    "UserEnvelope",
    "UserListEnvelope",
]
