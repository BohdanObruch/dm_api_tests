from __future__ import annotations

from datetime import datetime

from src.api.models.game.common_model import BadRequestError, CommonBbText, GeneralError, User
from src.api.models.shared.base_model import ApiIgnoreModel, ResourceEnvelope, ResourceListEnvelope


class Comment(ApiIgnoreModel):
    id: str | None = None
    author: User | None = None
    created: datetime | None = None
    updated: datetime | None = None
    text: CommonBbText | None = None
    likes: list[User] | None = None


CommentEnvelope = ResourceEnvelope[Comment]
CommentListEnvelope = ResourceListEnvelope[Comment]
UserEnvelope = ResourceEnvelope[User]


__all__ = [
    "BadRequestError",
    "Comment",
    "CommentEnvelope",
    "CommentListEnvelope",
    "GeneralError",
    "User",
    "UserEnvelope",
]
