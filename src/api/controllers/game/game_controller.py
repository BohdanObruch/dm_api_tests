from __future__ import annotations

from src.api.controllers.base_controller import BaseController
from src.api.models.game.game_model import (
    GameEnvelope,
    GameListEnvelope,
    TagListEnvelope,
    UserEnvelope,
    UserListEnvelope,
)


class GameApi(BaseController):
    def get_games(
        self,
        statuses: list[str] | None = None,
        tag: list[str] | None = None,
        skip: int | None = None,
        number: int | None = None,
        size: int | None = None,
    ) -> GameListEnvelope:
        params = {
            "statuses": statuses,
            "tag": tag,
            "skip": skip,
            "number": number,
            "size": size,
        }
        data = self._get("/v1/games", params=params)
        return GameListEnvelope.model_validate(data)

    def post_game(self, payload: dict) -> GameEnvelope:
        data = self._post("/v1/games", data=payload)
        return GameEnvelope.model_validate(data)

    def get_own_games(self) -> GameListEnvelope:
        data = self._get("/v1/games/own")
        return GameListEnvelope.model_validate(data)

    def get_popular_games(self) -> GameListEnvelope:
        data = self._get("/v1/games/popular")
        return GameListEnvelope.model_validate(data)

    def get_tags(self) -> TagListEnvelope:
        data = self._get("/v1/games/tags")
        return TagListEnvelope.model_validate(data)

    def get_game(self, id: str) -> GameEnvelope:
        data = self._get(f"/v1/games/{id}")
        return GameEnvelope.model_validate(data)

    def delete_game(self, id: str) -> None:
        self._delete(f"/v1/games/{id}")

    def get_game_details(self, id: str) -> GameEnvelope:
        data = self._get(f"/v1/games/{id}/details")
        return GameEnvelope.model_validate(data)

    def put_game(self, id: str, payload: dict) -> GameEnvelope:
        data = self._patch(f"/v1/games/{id}/details", data=payload)
        return GameEnvelope.model_validate(data)

    def get_readers(self, id: str) -> UserListEnvelope:
        data = self._get(f"/v1/games/{id}/readers")
        return UserListEnvelope.model_validate(data)

    def post_reader(self, id: str) -> UserEnvelope:
        data = self._post(f"/v1/games/{id}/readers")
        return UserEnvelope.model_validate(data)

    def delete_reader(self, id: str) -> None:
        self._delete(f"/v1/games/{id}/readers")

    def get_blacklist(self, id: str) -> UserListEnvelope:
        data = self._get(f"/v1/games/{id}/blacklist/users")
        return UserListEnvelope.model_validate(data)

    def post_blacklist(self, id: str, payload: dict) -> UserEnvelope:
        data = self._post(f"/v1/games/{id}/blacklist/users", data=payload)
        return UserEnvelope.model_validate(data)

    def delete_blacklist(self, id: str, login: str) -> None:
        self._delete(f"/v1/games/{id}/blacklist/users/{login}")
