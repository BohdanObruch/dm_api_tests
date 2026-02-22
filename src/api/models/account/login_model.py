from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from src.api.models.community.common_model import BadRequestError, GeneralError
from src.api.models.community.common_model import User as BaseUser
from src.api.models.shared.base_model import ResourceEnvelope


class LoginCredentials(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    login: str | None = None
    password: str | None = None
    remember_me: bool = Field(alias="rememberMe")


class User(BaseUser):
    pass


UserEnvelope = ResourceEnvelope[User]


__all__ = [
    "BadRequestError",
    "GeneralError",
    "LoginCredentials",
    "User",
    "UserEnvelope",
]
