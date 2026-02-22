from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from src.api.models.community.common_model import BadRequestError, CommonBbText, GeneralError, User
from src.api.models.shared.base_model import ResourceEnvelope, ResourceListEnvelope


class Review(BaseModel):
    id: str | None = None
    author: User | None = None
    created: datetime | None = None
    approved: bool | None = None
    text: CommonBbText | str | None = None


ReviewListEnvelope = ResourceListEnvelope[Review]
ReviewEnvelope = ResourceEnvelope[Review]


__all__ = [
    "BadRequestError",
    "GeneralError",
    "Review",
    "ReviewEnvelope",
    "ReviewListEnvelope",
]
