from __future__ import annotations

from pydantic import BaseModel, Field

from src.api.models.community.common_model import (
    BadRequestError,
    BbParseMode,
    ColorSchema,
    GeneralError,
    InfoBbText,
    PagingSettings,
    Rating,
    UserRole,
    UserSettings,
)
from src.api.models.community.common_model import (
    User as BaseUser,
)
from src.api.models.community.common_model import (
    UserDetails as BaseUserDetails,
)
from src.api.models.shared.base_model import ResourceEnvelope


class Registration(BaseModel):
    login: str | None = None
    email: str | None = None
    password: str | None = None


class ResetPassword(BaseModel):
    login: str | None = None
    email: str | None = None


class ChangePassword(BaseModel):
    login: str | None = None
    token: str | None = Field(default=None, json_schema_extra={"format": "uuid"})
    old_password: str | None = Field(default=None, alias="oldPassword")
    new_password: str | None = Field(default=None, alias="newPassword")


class ChangeEmail(BaseModel):
    login: str | None = None
    password: str | None = None
    email: str | None = None


class UserDetails(BaseUserDetails):
    pass


class User(BaseUser):
    token: str | None = Field(default=None, json_schema_extra={"format": "uuid"})
    email: str | None = None


UserDetailsEnvelope = ResourceEnvelope[UserDetails]
UserEnvelope = ResourceEnvelope[User]


__all__ = [
    "BadRequestError",
    "BbParseMode",
    "ChangeEmail",
    "ChangePassword",
    "ColorSchema",
    "GeneralError",
    "InfoBbText",
    "PagingSettings",
    "Rating",
    "Registration",
    "ResetPassword",
    "User",
    "UserDetails",
    "UserDetailsEnvelope",
    "UserEnvelope",
    "UserRole",
    "UserSettings",
]
