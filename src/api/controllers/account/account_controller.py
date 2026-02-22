from __future__ import annotations

from src.api.controllers.base_controller import BaseController
from src.api.models.account.account_model import (
    UserDetailsEnvelope,
    UserEnvelope,
)


class AccountApi(BaseController):
    def register(self, payload: dict) -> UserEnvelope:
        data = self._post("/v1/account", data=payload)
        return UserEnvelope.model_validate(data)

    def get_current_user(self) -> UserDetailsEnvelope:
        data = self._get("/v1/account")
        return UserDetailsEnvelope.model_validate(data)

    def activate(self, token: str, payload: dict | None = None) -> UserEnvelope:
        data = self._put(f"/v1/account/{token}", data=payload)
        return UserEnvelope.model_validate(data)

    def reset_password(self, payload: dict) -> UserEnvelope | dict:
        data = self._post("/v1/account/password", data=payload)
        if isinstance(data, dict) and data.get("resource"):
            return UserEnvelope.model_validate(data)
        return data

    def change_password(self, payload: dict) -> UserEnvelope:
        data = self._put("/v1/account/password", data=payload)
        return UserEnvelope.model_validate(data)

    def change_email(self, payload: dict) -> UserEnvelope:
        data = self._put("/v1/account/email", data=payload)
        return UserEnvelope.model_validate(data)
