from __future__ import annotations

from src.api.models.community.common_model import BadRequestError, GeneralError, Paging, User, UserDetails
from src.api.models.shared.base_model import ResourceEnvelope, ResourceListEnvelope

UserListEnvelope = ResourceListEnvelope[User]
UserEnvelope = ResourceEnvelope[User]
UserDetailsEnvelope = ResourceEnvelope[UserDetails]


__all__ = [
    "BadRequestError",
    "GeneralError",
    "Paging",
    "User",
    "UserDetails",
    "UserDetailsEnvelope",
    "UserEnvelope",
    "UserListEnvelope",
]
