from __future__ import annotations

from src.api.models.game.common_model import (
    Alignment,
    BadRequestError,
    Character,
    CharacterAttribute,
    CharacterPrivacySettings,
    CharacterStatus,
    GeneralError,
    GuidOptional,
    PendingPost,
    Room,
    RoomAccessPolicy,
    RoomAccessType,
    RoomClaim,
    RoomType,
    User,
)
from src.api.models.shared.base_model import ResourceEnvelope, ResourceListEnvelope

RoomEnvelope = ResourceEnvelope[Room]
RoomClaimEnvelope = ResourceEnvelope[RoomClaim]
PendingPostEnvelope = ResourceEnvelope[PendingPost]
RoomListEnvelope = ResourceListEnvelope[Room]


__all__ = [
    "Alignment",
    "BadRequestError",
    "Character",
    "CharacterAttribute",
    "CharacterPrivacySettings",
    "CharacterStatus",
    "GeneralError",
    "GuidOptional",
    "PendingPost",
    "PendingPostEnvelope",
    "Room",
    "RoomAccessPolicy",
    "RoomAccessType",
    "RoomClaim",
    "RoomClaimEnvelope",
    "RoomEnvelope",
    "RoomListEnvelope",
    "RoomType",
    "User",
]
