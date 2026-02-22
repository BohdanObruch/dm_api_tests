from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from src.api.models.community.common_model import BadRequestError, GeneralError
from src.api.models.shared.base_model import ResourceEnvelope, ResourceListEnvelope


class PollOption(BaseModel):
    id: str | None = None
    text: str | None = None
    votes_count: int | None = None
    voted: bool | None = None


class Poll(BaseModel):
    id: str | None = None
    ends: datetime | None = None
    title: str | None = None
    options: list[PollOption] | None = None


PollListEnvelope = ResourceListEnvelope[Poll]
PollEnvelope = ResourceEnvelope[Poll]


__all__ = [
    "BadRequestError",
    "GeneralError",
    "Poll",
    "PollEnvelope",
    "PollListEnvelope",
]
