from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from src.api.models.shared.base_model import (
    BadRequestError as SharedBadRequestError,
)
from src.api.models.shared.base_model import (
    GeneralError as SharedGeneralError,
)
from src.api.models.shared.base_model import (
    Paging as SharedPaging,
)
from src.api.models.shared.user_model import (
    BbParseMode as SharedBbParseMode,
)
from src.api.models.shared.user_model import (
    CommonBbText as SharedCommonBbText,
)
from src.api.models.shared.user_model import (
    Rating as SharedRating,
)
from src.api.models.shared.user_model import (
    User as SharedUser,
)
from src.api.models.shared.user_model import (
    UserRole as SharedUserRole,
)

Paging = SharedPaging
UserRole = SharedUserRole
BbParseMode = SharedBbParseMode
Rating = SharedRating
User = SharedUser
CommonBbText = SharedCommonBbText
GeneralError = SharedGeneralError
BadRequestError = SharedBadRequestError


class SchemaType(str, Enum):
    Public = "Public"
    Private = "Private"


class AttributeSpecificationType(str, Enum):
    Number = "Number"
    String = "String"
    List = "List"


class AttributeValueSpecification(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    value: str | None = None
    modifier: int | None = None


class AttributeSpecification(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    id: str | None = None
    title: str | None = None
    required: bool | None = None
    type: AttributeSpecificationType | None = None
    min_value: int | None = Field(default=None, alias="minValue")
    max_value: int | None = Field(default=None, alias="maxValue")
    max_length: int | None = Field(default=None, alias="maxLength")
    values: list[AttributeValueSpecification] | None = None


class AttributeSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    id: str | None = None
    title: str | None = None
    author: User | None = None
    type: SchemaType | None = None
    specifications: list[AttributeSpecification] | None = None


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


class GuidOptional(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    value: str | None = None


class CharacterAttribute(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    id: str | None = None
    title: str | None = None
    value: str | None = None
    modifier: int | None = None
    inconsistent: bool | None = None


class CharacterPrivacySettings(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    is_npc: bool | None = Field(default=None, alias="isNpc")
    edit_by_master: bool | None = Field(default=None, alias="editByMaster")
    edit_post_by_master: bool | None = Field(default=None, alias="editPostByMaster")


class Character(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    id: str | None = None
    author: User | None = None
    status: CharacterStatus | None = None
    total_posts_count: int | None = Field(default=None, alias="totalPostsCount")
    title: str | None = None
    name: str | None = None
    race: str | None = None
    class_: str | None = Field(default=None, alias="class")
    alignment: Alignment | None = None
    picture_url: str | None = Field(default=None, alias="pictureUrl")
    appearance: str | None = None
    temper: str | None = None
    story: str | None = None
    skills: str | None = None
    inventory: str | None = None
    attributes: list[CharacterAttribute] | None = None
    privacy: CharacterPrivacySettings | None = None


class RoomClaim(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    id: str | None = None
    policy: RoomAccessPolicy | None = None
    character: Character | None = None
    user: User | None = None


class PendingPost(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    id: str | None = None
    awaiting: User | None = None
    pending: User | None = None
    waits_since: datetime | None = Field(default=None, alias="waitsSince")


class Room(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    id: str | None = None
    previous_room_id: GuidOptional | None = Field(default=None, alias="previousRoomId")
    title: str | None = None
    access: RoomAccessType | None = None
    type: RoomType | None = None
    claims: list[RoomClaim] | None = None
    pendings: list[PendingPost] | None = None
    unread_posts_count: int | None = Field(default=None, alias="unreadPostsCount")


class VoteSign(str, Enum):
    Neutral = "Neutral"
    Positive = "Positive"
    Negative = "Negative"


class VoteType(str, Enum):
    Unknown = "Unknown"
    Fun = "Fun"
    Roleplay = "Roleplay"
    Literature = "Literature"
