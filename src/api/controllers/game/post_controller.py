from src.api.controllers.base_controller import BaseController
from src.api.models.game.post_model import (
    PostEnvelope,
    PostListEnvelope,
    VoteEnvelope,
    VoteListEnvelope,
)


class PostApi(BaseController):
    def get_posts(
        self,
        room_id: str,
        skip: int | None = None,
        number: int | None = None,
        size: int | None = None,
    ) -> PostListEnvelope:
        params = {
            "skip": skip,
            "number": number,
            "size": size,
        }
        data = self._get(f"/v1/rooms/{room_id}/posts", params=params)
        return PostListEnvelope.model_validate(data)

    def post_post(self, room_id: str, payload: dict) -> PostEnvelope:
        data = self._post(f"/v1/rooms/{room_id}/posts", data=payload)
        return PostEnvelope.model_validate(data)

    def mark_posts_as_read(self, room_id: str) -> None:
        self._delete(f"/v1/rooms/{room_id}/posts/unread")

    def get_post(self, post_id: str) -> PostEnvelope:
        data = self._get(f"/v1/posts/{post_id}")
        return PostEnvelope.model_validate(data)

    def put_post(self, post_id: str, payload: dict) -> PostEnvelope:
        data = self._patch(f"/v1/posts/{post_id}", data=payload)
        return PostEnvelope.model_validate(data)

    def delete_post(self, post_id: str) -> None:
        self._delete(f"/v1/posts/{post_id}")

    def get_post_votes(self, post_id: str) -> VoteListEnvelope:
        data = self._get(f"/v1/posts/{post_id}/votes")
        return VoteListEnvelope.model_validate(data)

    def post_vote(self, post_id: str, payload: dict) -> VoteEnvelope:
        data = self._post(f"/v1/posts/{post_id}/votes", data=payload)
        return VoteEnvelope.model_validate(data)
