from __future__ import annotations

from src.api.controllers.base_controller import BaseController
from src.api.models.forum.topic_model import CommentEnvelope, CommentListEnvelope, TopicEnvelope, UserEnvelope


class TopicController(BaseController):
    def get_topic(self, id: str) -> TopicEnvelope:
        data = self._get(f"/v1/topics/{id}")
        return TopicEnvelope.model_validate(data)

    def put_topic(self, id: str, payload: dict) -> TopicEnvelope:
        data = self._patch(f"/v1/topics/{id}", data=payload)
        return TopicEnvelope.model_validate(data)

    def delete_topic(self, id: str) -> dict | None:
        return self._delete(f"/v1/topics/{id}")

    def post_topic_like(self, id: str) -> UserEnvelope:
        data = self._post(f"/v1/topics/{id}/likes")
        return UserEnvelope.model_validate(data)

    def delete_topic_like(self, id: str) -> dict | None:
        return self._delete(f"/v1/topics/{id}/likes")

    def get_forum_comments(
        self, id: str, skip: int | None = None, number: int | None = None, size: int | None = None
    ) -> CommentListEnvelope:
        params = {}
        if skip is not None:
            params["skip"] = skip
        if number is not None:
            params["number"] = number
        if size is not None:
            params["size"] = size
        data = self._get(f"/v1/topics/{id}/comments", params=params)
        return CommentListEnvelope.model_validate(data)

    def post_forum_comment(self, id: str, payload: dict) -> CommentEnvelope:
        data = self._post(f"/v1/topics/{id}/comments", data=payload)
        return CommentEnvelope.model_validate(data)

    def read_topic_comments(self, id: str) -> dict | None:
        return self._delete(f"/v1/topics/{id}/comments/unread")
