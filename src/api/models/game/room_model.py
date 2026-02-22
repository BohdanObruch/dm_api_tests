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


class RoomAccessType(str, Enum):
    Open = "Open"
    Secret = "Secret"
    Archive = "Archive"


class RoomType(str, Enum):
    Default = "Default"
    Chat = "Chat"


class RoomAccessPolicy(str, Enum):
    NoAccess = "NoAccess"
    ReadOnly = "ReadOnly"
    Full = "Full"


class CharacterStatus(str, Enum):
    Registration = "Registration"
    Declined = "Declined"
    Active = "Active"
    Dead = "Dead"
    Left = "Left"


class Alignment(str, Enum):
    LawfulGood = "LawfulGood"
    NeutralGood = "NeutralGood"
    ChaoticGood = "ChaoticGood"
    LawfulNeutral = "LawfulNeutral"
    TrueNeutral = "TrueNeutral"
    ChaoticNeutral = "ChaoticNeutral"
    LawfulEvil = "LawfulEvil"
    NeutralEvil = "NeutralEvil"
    ChaoticEvil = "ChaoticEvil"


class UserRole(str, Enum):
    Guest = "Guest"
    Player = "Player"
    Administrator = "Administrator"
    NannyModerator = "NannyModerator"
    RegularModerator = "RegularModerator"
    SeniorModerator = "SeniorModerator"


class GuidOptional(BaseModel):
    model_config = ConfigDict(extra="allow")

    value: str | None = None


class GeneralError(BaseModel):
    model_config = ConfigDict(extra="allow")

    message: str | None = None


class BadRequestError(BaseModel):
    model_config = ConfigDict(extra="allow")

    message: str | None = None
    invalid_properties: dict[str, list[str]] | None = Field(default=None, alias="invalidProperties")


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


class CharacterAttribute(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    title: str | None = None
    value: str | None = None
    modifier: int | None = None
    inconsistent: bool | None = None


class CharacterPrivacySettings(BaseModel):
    model_config = ConfigDict(extra="allow")

    is_npc: bool | None = Field(default=None, alias="isNpc")
    edit_by_master: bool | None = Field(default=None, alias="editByMaster")
    edit_post_by_master: bool | None = Field(default=None, alias="editPostByMaster")


class Character(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    author: User | None = None
    status: CharacterStatus | None = None
    total_posts_count: int | None = Field(default=None, alias="totalPostsCount")
    title: str | None = None
    name: str | None = None
    race: str | None = None
    class_: str | None = Field(default=None, alias="class")
    alignment: Alignment | None = None
    attributes: list[CharacterAttribute] | None = None
    privacy: CharacterPrivacySettings | None = None


class RoomClaim(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    policy: RoomAccessPolicy | None = None
    character: Character | None = None
    user: User | None = None


class PendingPost(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    awaiting: User | None = None
    pending: User | None = None
    waits_since: datetime | None = Field(default=None, alias="waitsSince")


class Room(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    previous_room_id: GuidOptional | None = Field(default=None, alias="previousRoomId")
    title: str | None = None
    access: RoomAccessType | None = None
    type: RoomType | None = None
    claims: list[RoomClaim] | None = None
    pendings: list[PendingPost] | None = None
    unread_posts_count: int | None = Field(default=None, alias="unreadPostsCount")


class RoomEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow")

    resource: Room | None = None
    metadata: dict | None = None


class RoomClaimEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow")

    resource: RoomClaim | None = None
    metadata: dict | None = None


class PendingPostEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow")

    resource: PendingPost | None = None
    metadata: dict | None = None


class RoomListEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow")

    resources: list[Room] | None = None
    paging: Paging | None = None
