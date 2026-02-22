from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class CharacterListEnvelope(BaseModel):
    resources: list[Character] | None = None
    paging: Paging | None = None


class GeneralError(BaseModel):
    message: str | None = None


class Character(BaseModel):
    id: str
    author: User | None = None
    status: CharacterStatus | None = None
    totalPostsCount: int | None = Field(None, alias="totalPostsCount")
    name: str | None = None
    race: str | None = None
    class_: str | None = Field(None, alias="class")
    alignment: Alignment | None = None
    pictureUrl: str | None = Field(None, alias="pictureUrl")
    appearance: str | None = None
    temper: str | None = None
    story: str | None = None
    skills: str | None = None
    inventory: str | None = None
    attributes: list[CharacterAttribute] | None = None
    privacy: CharacterPrivacySettings | None = None


class CharacterEnvelope(BaseModel):
    resource: Character | None = None
    metadata: dict | None = None


class BadRequestError(BaseModel):
    message: str | None = None
    invalidProperties: dict[str, list[str]] | None = Field(None, alias="invalidProperties")


class Paging(BaseModel):
    pages: int | None = None
    current: int | None = None
    size: int | None = None
    number: int | None = None
    total: int | None = None


class User(BaseModel):
    login: str | None = None
    roles: list[UserRole] | None = None
    mediumPictureUrl: str | None = Field(None, alias="mediumPictureUrl")
    smallPictureUrl: str | None = Field(None, alias="smallPictureUrl")
    status: str | None = None
    rating: Rating | None = None
    online: datetime | None = None
    name: str | None = None
    location: str | None = None
    registration: datetime | None = None


class CharacterStatus(str):
    Registration = "Registration"
    Declined = "Declined"
    Active = "Active"
    Dead = "Dead"
    Left = "Left"


class Alignment(str):
    LawfulGood = "LawfulGood"
    NeutralGood = "NeutralGood"
    ChaoticGood = "ChaoticGood"
    LawfulNeutral = "LawfulNeutral"
    TrueNeutral = "TrueNeutral"
    ChaoticNeutral = "ChaoticNeutral"
    LawfulEvil = "LawfulEvil"
    NeutralEvil = "NeutralEvil"
    ChaoticEvil = "ChaoticEvil"


class CharacterAttribute(BaseModel):
    id: str
    title: str | None = None
    value: str | None = None
    modifier: int | None = None
    inconsistent: bool | None = None


class CharacterPrivacySettings(BaseModel):
    isNpc: bool = Field(..., alias="isNpc")
    editByMaster: bool = Field(..., alias="editByMaster")
    editPostByMaster: bool = Field(..., alias="editPostByMaster")


class UserRole(str):
    Guest = "Guest"
    Player = "Player"
    Administrator = "Administrator"
    NannyModerator = "NannyModerator"
    RegularModerator = "RegularModerator"
    SeniorModerator = "SeniorModerator"


class Rating(BaseModel):
    enabled: bool | None = None
    quality: int | None = None
    quantity: int | None = None
