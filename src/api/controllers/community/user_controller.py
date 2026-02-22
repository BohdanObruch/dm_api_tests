from __future__ import annotations

from src.api.controllers.base_controller import BaseController
from src.api.models.community.user_model import UserDetailsEnvelope, UserEnvelope, UserListEnvelope


class UserApi(BaseController):
    def list(
        self,
        inactive: bool | None = None,
        skip: int | None = None,
        number: int | None = None,
        size: int | None = None,
    ) -> UserListEnvelope:
        params = {
            "inactive": inactive,
            "skip": skip,
            "number": number,
            "size": size,
        }
        data = self._get("/v1/users", params=params)
        return UserListEnvelope.model_validate(data)

    def get_by_login(self, login: str) -> UserEnvelope:
        data = self._get(f"/v1/users/{login}")
        return UserEnvelope.model_validate(data)

    def get_details_by_login(self, login: str) -> UserDetailsEnvelope:
        data = self._get(f"/v1/users/{login}/details")
        return UserDetailsEnvelope.model_validate(data)

    def update_details_by_login(self, login: str, payload: dict) -> UserDetailsEnvelope:
        data = self._patch(f"/v1/users/{login}/details", data=payload)
        return UserDetailsEnvelope.model_validate(data)
