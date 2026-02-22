from __future__ import annotations

from src.api.controllers.base_controller import BaseController
from src.api.models.community.userupload_model import UserDetailsEnvelope


class UserUploadApi(BaseController):
    def post_user_upload(self, login: str, file: bytes, render_mode: str | None = None) -> UserDetailsEnvelope:
        files = {"file": ("upload.png", file, "image/png")}
        headers = {}
        if render_mode:
            headers["X-Dm-Bb-Render-Mode"] = render_mode
        data = self._post(f"/v1/users/{login}/uploads", files=files, headers=headers)
        return UserDetailsEnvelope.model_validate(data)
