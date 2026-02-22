from __future__ import annotations

from src.api.controllers.base_controller import BaseController
from src.api.models.forum.forum_model import (
    ForumEnvelope,
    ForumListEnvelope,
    TopicEnvelope,
    TopicListEnvelope,
    UserListEnvelope,
)


class ForumApi(BaseController):
    def get_fora(self) -> ForumListEnvelope:
        data = self._get("/v1/fora")
        return ForumListEnvelope.model_validate(data)

    def get_forum(self, id: str) -> ForumEnvelope:
        data = self._get(f"/v1/fora/{id}")
        return ForumEnvelope.model_validate(data)

    def read_forum_comments(self, id: str) -> None:
        self._delete(f"/v1/fora/{id}/comments/unread")

    def get_moderators(self, id: str) -> UserListEnvelope:
        data = self._get(f"/v1/fora/{id}/moderators")
        return UserListEnvelope.model_validate(data)

    def get_topics(
        self,
        id: str,
        attached: bool | None = None,
        skip: int | None = None,
        number: int | None = None,
        size: int | None = None,
    ) -> TopicListEnvelope:
        params = {
            "attached": attached,
            "skip": skip,
            "number": number,
            "size": size,
        }
        data = self._get(f"/v1/fora/{id}/topics", params=params)
        return TopicListEnvelope.model_validate(data)

    def post_topic(self, id: str, payload: dict) -> TopicEnvelope:
        data = self._post(f"/v1/fora/{id}/topics", data=payload)
        return TopicEnvelope.model_validate(data)
