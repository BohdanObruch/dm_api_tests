from __future__ import annotations

from src.api.controllers.base_controller import BaseController
from src.api.models.account.login_model import LoginCredentials, UserEnvelope


class LoginApi(BaseController):
    def login(self, payload: LoginCredentials, x_dm_bb_render_mode: str | None = None) -> UserEnvelope:
        headers = {}
        if x_dm_bb_render_mode is not None:
            headers["X-Dm-Bb-Render-Mode"] = x_dm_bb_render_mode

        response = self._session.post(
            self._url("/v1/account/login"),
            headers=self._headers(content_type=True, extra_headers=headers),
            json=payload.model_dump(by_alias=True, exclude_none=True),
            timeout=30,
        )
        response.raise_for_status()
        data = self._response_json(response)
        if not isinstance(data, dict):
            data = {}

        metadata = data.get("metadata")
        if not isinstance(metadata, dict):
            metadata = {}
        token = response.headers.get("X-Dm-Auth-Token")
        if token and "token" not in metadata:
            metadata["token"] = token
        if metadata:
            data["metadata"] = metadata

        return UserEnvelope.model_validate(data)

    def logout(self, x_dm_auth_token: str, x_dm_bb_render_mode: str | None = None) -> None:
        headers = {"X-Dm-Auth-Token": x_dm_auth_token}
        if x_dm_bb_render_mode is not None:
            headers["X-Dm-Bb-Render-Mode"] = x_dm_bb_render_mode
        self._delete("/v1/account/login", headers=headers)

    def logout_all(self, x_dm_auth_token: str, x_dm_bb_render_mode: str | None = None) -> None:
        headers = {"X-Dm-Auth-Token": x_dm_auth_token}
        if x_dm_bb_render_mode is not None:
            headers["X-Dm-Bb-Render-Mode"] = x_dm_bb_render_mode
        self._delete("/v1/account/login/all", headers=headers)
