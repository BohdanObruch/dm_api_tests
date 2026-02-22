from __future__ import annotations

from enum import Enum

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


class ColorSchema(str, Enum):
    Modern = "Modern"
    Pale = "Pale"
    Classic = "Classic"
    ClassicPale = "ClassicPale"
    Night = "Night"


class InfoBbText(SharedCommonBbText):
    pass


class PagingSettings(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    posts_per_page: int | None = Field(default=None, alias="postsPerPage")
    comments_per_page: int | None = Field(default=None, alias="commentsPerPage")
    topics_per_page: int | None = Field(default=None, alias="topicsPerPage")
    messages_per_page: int | None = Field(default=None, alias="messagesPerPage")
    entities_per_page: int | None = Field(default=None, alias="entitiesPerPage")


class UserSettings(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    color_schema: ColorSchema | None = Field(default=None, alias="colorSchema")
    nanny_greetings_message: str | None = Field(default=None, alias="nannyGreetingsMessage")
    paging: PagingSettings | None = None


class UserDetails(SharedUser):
    icq: str | None = None
    skype: str | None = None
    original_picture_url: str | None = Field(default=None, alias="originalPictureUrl")
    info: InfoBbText | str | None = None
    settings: UserSettings | None = None


Paging = SharedPaging
UserRole = SharedUserRole
BbParseMode = SharedBbParseMode
Rating = SharedRating
User = SharedUser
CommonBbText = SharedCommonBbText
GeneralError = SharedGeneralError
BadRequestError = SharedBadRequestError
