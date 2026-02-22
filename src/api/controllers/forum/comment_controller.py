from src.api.controllers.base_controller import BaseController
from src.api.models.forum.comment_model import CommentEnvelope, UserEnvelope


class CommentController(BaseController):
    def get_comment(self, id: str, render_mode: str | None = None) -> CommentEnvelope:
        headers = {}
        if render_mode:
            headers["X-Dm-Bb-Render-Mode"] = render_mode
        data = self._get(f"/v1/forum/comments/{id}", headers=headers)
        return CommentEnvelope.model_validate(data)

    def update_comment(self, id: str, payload: dict, render_mode: str | None = None) -> CommentEnvelope:
        headers = {}
        if render_mode:
            headers["X-Dm-Bb-Render-Mode"] = render_mode
        data = self._patch(f"/v1/forum/comments/{id}", data=payload, headers=headers)
        return CommentEnvelope.model_validate(data)

    def delete_comment(self, id: str, render_mode: str | None = None) -> dict | None:
        headers = {}
        if render_mode:
            headers["X-Dm-Bb-Render-Mode"] = render_mode
        return self._delete(f"/v1/forum/comments/{id}", headers=headers)

    def like_comment(self, id: str, render_mode: str | None = None) -> UserEnvelope:
        headers = {}
        if render_mode:
            headers["X-Dm-Bb-Render-Mode"] = render_mode
        data = self._post(f"/v1/forum/comments/{id}/likes", headers=headers)
        return UserEnvelope.model_validate(data)

    def unlike_comment(self, id: str, render_mode: str | None = None) -> dict | None:
        headers = {}
        if render_mode:
            headers["X-Dm-Bb-Render-Mode"] = render_mode
        return self._delete(f"/v1/forum/comments/{id}/likes", headers=headers)
