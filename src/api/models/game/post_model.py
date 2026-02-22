from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class PostListEnvelope(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    resources: list[Post] | None = Field(default=None, description="Enveloped resources")
    paging: Paging | None = None


class GeneralError(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    message: str | None = Field(default=None, description="Client message")


class Post(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str | None = Field(default=None, description="Post identifier", examples=["123e4567-e89b-12d3-a456-426614174000"], pattern=r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
    room: Room | None = None
    character: Character | None = None
    author: User | None = None
    created: datetime | None = Field(default=None, description="Creation moment", examples=["2023-10-26T10:00:00Z"])
    updated: datetime | None = Field(default=None, description="Last update moment", examples=["2023-10-26T10:00:00Z"])
    text: PostBbText | None = None
    commentary: CommonBbText | None = None
    master_message: CommonBbText | None = Field(None, alias="masterMessage")
    dice_rolls: list[DiceRoll] | None = Field(default=None, alias="diceRolls", description="Dice roll results")


class PostEnvelope(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    resource: Post | None = None
    metadata: dict[str, Any] | None = Field(default=None, description="Additional metadata")


class BadRequestError(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    message: str | None = Field(default=None, description="Client message")
    invalid_properties: dict[str, list[str]] | None = Field(default=None, alias="invalidProperties", description="Key-value pairs of invalid request properties")


class VoteListEnvelope(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    resources: list[Vote] | None = Field(default=None, description="Enveloped resources")
    paging: Paging | None = None


class Vote(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    post: Post | None = None
    author: User | None = None
    sign: VoteSign | None = None
    type: VoteType | None = None
    text: CommonBbText | None = None
    created: datetime | None = Field(default=None, description="Creation moment", examples=["2023-10-26T10:00:00Z"])


class VoteEnvelope(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    resource: Vote | None = None
    metadata: dict[str, Any] | None = Field(default=None, description="Additional metadata")


class Paging(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    pages: int | None = Field(default=None, description="Total pages count", json_schema_extra={"read_only": True})
    current: int | None = Field(default=None, description="Current page number", json_schema_extra={"read_only": True})
    size: int | None = Field(default=None, description="Page size", json_schema_extra={"read_only": True})
    number: int | None = Field(default=None, description="Entity number", json_schema_extra={"read_only": True})
    total: int | None = Field(default=None, description="Total entity count", json_schema_extra={"read_only": True})


class Room(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str | None = Field(default=None, description="Room identifier", examples=["123e4567-e89b-12d3-a456-426614174000"], pattern=r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
    previous_room_id: GuidOptional | None = Field(default=None, alias="previousRoomId")
    title: str | None = Field(default=None, description="Room title")
    access: RoomAccessType | None = None
    type: RoomType | None = None
    claims: list[RoomClaim] | None = Field(default=None, description="Room claims")
    pendings: list[PendingPost] | None = Field(default=None, description="Post pendings")
    unread_posts_count: int | None = Field(default=None, alias="unreadPostsCount", description="Number of unread posts")


class Character(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str | None = Field(default=None, description="Character identifier", examples=["123e4567-e89b-12d3-a456-426614174000"], pattern=r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
    author: User | None = None
    status: CharacterStatus | None = None
    total_posts_count: int | None = Field(default=None, alias="totalPostsCount", description="Total characters posts count")
    name: str | None = Field(default=None, description="Character name")
    race: str | None = Field(default=None, description="Character race")
    class_: str | None = Field(default=None, alias="class")
    alignment: Alignment | None = None
    picture_url: str | None = Field(default=None, alias="pictureUrl", description="Character picture URL")
    appearance: str | None = Field(default=None, description="Character appearance")
    temper: str | None = Field(default=None, description="Character temper")
    story: str | None = Field(default=None, description="Character story")
    skills: str | None = Field(default=None, description="Character skills")
    inventory: str | None = Field(default=None, description="Character inventory")
    attributes: list[CharacterAttribute] | None = Field(default=None, description="Character attributes")
    privacy: CharacterPrivacySettings | None = None


class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    login: str | None = Field(default=None, description="Login")
    roles: list[UserRole] | None = Field(default=None, description="Roles")
    medium_picture_url: str | None = Field(default=None, alias="mediumPictureUrl", description="Profile picture URL M-size")
    small_picture_url: str | None = Field(default=None, alias="smallPictureUrl", description="Profile picture URL S-size")
    status: str | None = Field(default=None, description="User defined status")
    rating: Rating | None = None
    online: datetime | None = Field(default=None, description="Last seen online moment", examples=["2023-10-26T10:00:00Z"])
    name: str | None = Field(default=None, description="User real name")
    location: str | None = Field(default=None, description="User real location")
    registration: datetime | None = Field(default=None, description="User registration moment", examples=["2023-10-26T10:00:00Z"])


class PostBbText(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    value: str | None = Field(default=None, description="Text")
    parse_mode: BbParseMode | None = Field(default=None, alias="parseMode")


class CommonBbText(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    value: str | None = Field(default=None, description="Text")
    parse_mode: BbParseMode | None = Field(default=None, alias="parseMode")


class DiceRoll(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    rolls: int | None = Field(default=None, description="Rolls count")
    edges: int | None = Field(default=None, description="Die edges count")
    bonus: int | None = Field(default=None, description="Additional bonus")
    blast: int | None = Field(default=None, description="Blasts count")
    comment: str | None = Field(default=None, description="Commentary")
    results: list[DiceResult] | None = Field(default=None, description="Results")


class GuidOptional(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    value: str | None = Field(
        default=None,
        pattern=r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$",
        json_schema_extra={"read_only": True},
    )


class RoomClaim(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str | None = Field(default=None, description="Claim identifier", examples=["123e4567-e89b-12d3-a456-426614174000"], pattern=r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
    policy: RoomAccessPolicy | None = None
    character: Character | None = None
    user: User | None = None


class PendingPost(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str | None = Field(default=None, description="Identifier", examples=["123e4567-e89b-12d3-a456-426614174000"], pattern=r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
    awaiting: User | None = None
    pending: User | None = None
    waits_since: datetime | None = Field(default=None, alias="waitsSince", description="Date since the post is being awaited", examples=["2023-10-26T10:00:00Z"])


class CharacterAttribute(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str | None = Field(default=None, description="Specification identifier", examples=["123e4567-e89b-12d3-a456-426614174000"], pattern=r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
    title: str | None = Field(default=None, description="Specification title")
    value: str | None = Field(default=None, description="Attribute value")
    modifier: int | None = Field(default=None, description="Attribute modifier")
    inconsistent: bool | None = Field(default=None, description="Flag of the required value missing")


class CharacterPrivacySettings(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    is_npc: bool | None = Field(default=None, alias="isNpc", description="Character is non-player-character")
    edit_by_master: bool | None = Field(default=None, alias="editByMaster", description="Character may be edited by master or assistant")
    edit_post_by_master: bool | None = Field(default=None, alias="editPostByMaster", description="Character's posts may be edited by master or assistant")


class Rating(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    enabled: bool | None = Field(default=None, description="Rating participation flag")
    quality: int | None = Field(default=None, description="Quality rating")
    quantity: int | None = Field(default=None, description="Quantity rating")


class DiceResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    value: int | None = Field(default=None, description="Roll result value")
    critical: bool | None = Field(default=None, description="Result was critical")
    blasted: bool | None = Field(default=None, description="Result has blasted")


class VoteSign(str, Enum):
    Neutral = "Neutral"
    Positive = "Positive"
    Negative = "Negative"


class VoteType(str, Enum):
    Unknown = "Unknown"
    Fun = "Fun"
    Roleplay = "Roleplay"
    Literature = "Literature"


class RoomAccessType(str, Enum):
    Open = "Open"
    Secret = "Secret"
    Archive = "Archive"


class RoomType(str, Enum):
    Default = "Default"
    Chat = "Chat"


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


class BbParseMode(str, Enum):
    Common = "Common"
    Info = "Info"
    Post = "Post"
    Chat = "Chat"


class RoomAccessPolicy(str, Enum):
    NoAccess = "NoAccess"
    ReadOnly = "ReadOnly"
    Full = "Full"


