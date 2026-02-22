from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.api.models.forum.forum_model import Forum, LastTopicComment, Topic
from src.api.models.shared.base_model import Paging, ResourceEnvelope, ResourceListEnvelope
from src.api.models.shared.user_model import CommonBbText, User


class Comment(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    author: User | None = None
    created: datetime | None = None
    updated: datetime | None = None
    text: CommonBbText | str | None = None
    likes: list[User] | None = None


TopicEnvelope = ResourceEnvelope[Topic]
UserEnvelope = ResourceEnvelope[User]
CommentEnvelope = ResourceEnvelope[Comment]
CommentListEnvelope = ResourceListEnvelope[Comment]


__all__ = [
    "Comment",
    "CommentEnvelope",
    "CommentListEnvelope",
    "Forum",
    "LastTopicComment",
    "Paging",
    "Topic",
    "TopicEnvelope",
    "User",
    "UserEnvelope",
]
