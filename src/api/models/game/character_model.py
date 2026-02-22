from __future__ import annotations

from src.api.models.game.common_model import (
    Alignment,
    BadRequestError,
    Character,
    CharacterAttribute,
    CharacterPrivacySettings,
    CharacterStatus,
    GeneralError,
    Rating,
    User,
    UserRole,
)
from src.api.models.shared.base_model import ResourceEnvelope, ResourceListEnvelope

CharacterListEnvelope = ResourceListEnvelope[Character]
CharacterEnvelope = ResourceEnvelope[Character]


__all__ = [
    "Alignment",
    "BadRequestError",
    "Character",
    "CharacterAttribute",
    "CharacterEnvelope",
    "CharacterListEnvelope",
    "CharacterPrivacySettings",
    "CharacterStatus",
    "GeneralError",
    "Rating",
    "User",
    "UserRole",
]
