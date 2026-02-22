from __future__ import annotations

from src.api.models.community.common_model import UserDetails
from src.api.models.shared.base_model import ResourceEnvelope

UserDetailsEnvelope = ResourceEnvelope[UserDetails]
