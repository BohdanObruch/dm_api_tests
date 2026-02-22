from __future__ import annotations

from datetime import datetime

from pydantic import Field

from src.api.models.game.common_model import (
    Alignment,
    BadRequestError,
    BbParseMode,
    Character,
    CharacterAttribute,
    CharacterPrivacySettings,
    CharacterStatus,
    CommonBbText,
    GeneralError,
    GuidOptional,
    PendingPost,
    Room,
    RoomAccessPolicy,
    RoomAccessType,
    RoomClaim,
    RoomType,
    User,
    VoteSign,
    VoteType,
)
from src.api.models.shared.base_model import ApiIgnoreModel, ResourceEnvelope, ResourceListEnvelope


class PostBbText(ApiIgnoreModel):
    value: str | None = None
    parse_mode: BbParseMode | None = Field(default=None, alias="parseMode")


class DiceResult(ApiIgnoreModel):
    value: int | None = None
    critical: bool | None = None
    blasted: bool | None = None


class DiceRoll(ApiIgnoreModel):
    rolls: int | None = None
    edges: int | None = None
    bonus: int | None = None
    blast: int | None = None
    comment: str | None = None
    results: list[DiceResult] | None = None


class Post(ApiIgnoreModel):
    id: str | None = None
    room: Room | None = None
    character: Character | None = None
    author: User | None = None
    created: datetime | None = None
    updated: datetime | None = None
    text: PostBbText | None = None
    commentary: CommonBbText | None = None
    master_message: CommonBbText | None = Field(default=None, alias="masterMessage")
    dice_rolls: list[DiceRoll] | None = Field(default=None, alias="diceRolls")


class Vote(ApiIgnoreModel):
    post: Post | None = None
    author: User | None = None
    sign: VoteSign | None = None
    type: VoteType | None = None
    text: CommonBbText | None = None
    created: datetime | None = None


PostEnvelope = ResourceEnvelope[Post]
PostListEnvelope = ResourceListEnvelope[Post]
VoteEnvelope = ResourceEnvelope[Vote]
VoteListEnvelope = ResourceListEnvelope[Vote]


__all__ = [
    "Alignment",
    "BadRequestError",
    "Character",
    "CharacterAttribute",
    "CharacterPrivacySettings",
    "CharacterStatus",
    "DiceResult",
    "DiceRoll",
    "GeneralError",
    "GuidOptional",
    "PendingPost",
    "Post",
    "PostBbText",
    "PostEnvelope",
    "PostListEnvelope",
    "Room",
    "RoomAccessPolicy",
    "RoomAccessType",
    "RoomClaim",
    "RoomType",
    "User",
    "Vote",
    "VoteEnvelope",
    "VoteListEnvelope",
    "VoteSign",
    "VoteType",
]
