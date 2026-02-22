from __future__ import annotations

from src.api.controllers.base_controller import BaseController
from src.api.models.game.character_model import CharacterEnvelope, CharacterListEnvelope


class CharacterApi(BaseController):
    def get_game_characters(self, id: str) -> CharacterListEnvelope:
        data = self._get(f"/v1/games/{id}/characters")
        return CharacterListEnvelope.model_validate(data)

    def post_character(self, id: str, payload: dict) -> CharacterEnvelope:
        data = self._post(f"/v1/games/{id}/characters", data=payload)
        return CharacterEnvelope.model_validate(data)

    def read_game_characters(self, id: str) -> None:
        self._delete(f"/v1/game/{id}/characters/unread")

    def get_character(self, id: str) -> CharacterEnvelope:
        data = self._get(f"/v1/characters/{id}")
        return CharacterEnvelope.model_validate(data)

    def put_character(self, id: str, payload: dict) -> CharacterEnvelope:
        data = self._patch(f"/v1/characters/{id}", data=payload)
        return CharacterEnvelope.model_validate(data)

    def delete_character(self, id: str) -> None:
        self._delete(f"/v1/characters/{id}")
