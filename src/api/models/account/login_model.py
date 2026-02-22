from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class LoginCredentials(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    login: str | None = None
    password: str | None = None
    remember_me: bool = Field(alias="rememberMe")


class BadRequestError(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    message: str | None = None
    invalid_properties: dict[str, list[str]] | None = Field(default=None, alias="invalidProperties")


class GeneralError(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    message: str | None = None


class Rating(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    enabled: bool
    quality: int
    quantity: int


class UserRole(StrEnum):
    GUEST = "Guest"
    PLAYER = "Player"
    ADMINISTRATOR = "Administrator"
    NANNY_MODERATOR = "NannyModerator"
    REGULAR_MODERATOR = "RegularModerator"
    SENIOR_MODERATOR = "SeniorModerator"


class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    login: str | None = None
    roles: list[UserRole] | None = None
    medium_picture_url: str | None = Field(default=None, alias="mediumPictureUrl")
    small_picture_url: str | None = Field(default=None, alias="smallPictureUrl")
    status: str | None = None
    rating: Rating
    online: datetime | None = None
    name: str | None = None
    location: str | None = None
    registration: datetime | None = None


class UserEnvelope(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    resource: User | None = None
    metadata: dict | None = None
