from __future__ import annotations

from src.api.controllers.base_controller import BaseController
from src.api.models.game.comment_model import (
    CommentEnvelope,
    CommentListEnvelope,
    UserEnvelope,
)


class CommentApi(BaseController):
    def get_game_comments(
        self,
        game_id: str,
        skip: int | None = None,
        number: int | None = None,
        size: int | None = None,
    ) -> CommentListEnvelope:
        """
        Get list of comments for a game.
        """
        params = {
            "skip": skip,
            "number": number,
            "size": size,
        }
        data = self._get(f"/v1/games/{game_id}/comments", params=params)
        return CommentListEnvelope.model_validate(data)

    def post_game_comment(self, game_id: str, payload: dict) -> CommentEnvelope:
        """
        Post a new game comment.
        """
        data = self._post(f"/v1/games/{game_id}/comments", data=payload)
        return CommentEnvelope.model_validate(data)

    def read_game_comments(self, game_id: str) -> None:
        """
        Mark all game comments as read.
        """
        self._delete(f"/v1/games/{game_id}/comments/unread")

    def get_game_comment(self, comment_id: str) -> CommentEnvelope:
        """
        Get a specific game comment.
        """
        data = self._get(f"/v1/games/comments/{comment_id}")
        return CommentEnvelope.model_validate(data)

    def update_game_comment(self, comment_id: str, payload: dict) -> CommentEnvelope:
        """
        Update a game comment.
        """
        data = self._patch(f"/v1/games/comments/{comment_id}", data=payload)
        return CommentEnvelope.model_validate(data)

    def delete_game_comment(self, comment_id: str) -> None:
        """
        Delete a game comment.
        """
        self._delete(f"/v1/games/comments/{comment_id}")

    def post_game_comment_like(self, comment_id: str) -> UserEnvelope:
        """
        Post a new like for a comment.
        """
        data = self._post(f"/v1/games/comments/{comment_id}/likes")
        return UserEnvelope.model_validate(data)

    def delete_game_comment_like(self, comment_id: str) -> None:
        """
        Delete a like from a comment.
        """
        self._delete(f"/v1/games/comments/{comment_id}/likes")
