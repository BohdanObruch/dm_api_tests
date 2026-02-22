from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.api.models.shared.base_model import (
    BadRequestError as SharedBadRequestError,
)
from src.api.models.shared.base_model import (
    GeneralError as SharedGeneralError,
)
from src.api.models.shared.base_model import (
    Paging as SharedPaging,
)
from src.api.models.shared.base_model import (
    ResourceEnvelope,
    ResourceListEnvelope,
)
from src.api.models.shared.user_model import (
    BbParseMode as SharedBbParseMode,
)
from src.api.models.shared.user_model import (
    CommonBbText as SharedCommonBbText,
)
from src.api.models.shared.user_model import (
    Rating as SharedRating,
)
from src.api.models.shared.user_model import (
    User as SharedUser,
)
from src.api.models.shared.user_model import (
    UserRole as SharedUserRole,
)

Paging = SharedPaging
UserRole = SharedUserRole
BbParseMode = SharedBbParseMode
Rating = SharedRating
User = SharedUser
CommonBbText = SharedCommonBbText
GeneralError = SharedGeneralError
BadRequestError = SharedBadRequestError


class Forum(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str | None = None
    unread_topics_count: int | None = Field(default=None, alias="unreadTopicsCount")


class LastTopicComment(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    created: datetime | None = None
    author: User | None = None


class Topic(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str | None = None
    author: User | None = None
    created: datetime | None = None
    title: str | None = None
    description: CommonBbText | str | None = None
    attached: bool | None = None
    closed: bool | None = None
    last_comment: LastTopicComment | None = Field(default=None, alias="lastComment")
    comments_count: int | None = Field(default=None, alias="commentsCount")
    unread_comments_count: int | None = Field(default=None, alias="unreadCommentsCount")
    forum: Forum | None = None
    likes: list[User] | None = None


ForumListEnvelope = ResourceListEnvelope[Forum]
ForumEnvelope = ResourceEnvelope[Forum]
UserListEnvelope = ResourceListEnvelope[User]
TopicListEnvelope = ResourceListEnvelope[Topic]
TopicEnvelope = ResourceEnvelope[Topic]
