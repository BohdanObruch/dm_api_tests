from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.api.models.forum.forum_model import CommonBbText, User
from src.api.models.shared.base_model import ResourceEnvelope


class Comment(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str | None = Field(default=None, alias="id")
    author: User | None = Field(default=None, alias="author")
    created: datetime | None = Field(default=None, alias="created")
    updated: datetime | None = Field(default=None, alias="updated")
    text: CommonBbText | str | None = Field(default=None, alias="text")
    likes: list[User] | None = Field(default=None, alias="likes")


CommentEnvelope = ResourceEnvelope[Comment]
UserEnvelope = ResourceEnvelope[User]


CommentEnvelope.model_rebuild()
Comment.model_rebuild()
UserEnvelope.model_rebuild()

