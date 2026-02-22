from __future__ import annotations

from src.api.controllers.base_controller import BaseController
from src.api.models.game.room_model import PendingPostEnvelope, RoomClaimEnvelope, RoomEnvelope, RoomListEnvelope


class RoomApi(BaseController):
    def get_rooms(self, game_id: str) -> RoomListEnvelope:
        data = self._get(f"/v1/games/{game_id}/rooms")
        return RoomListEnvelope.model_validate(data)

    def post_room(self, game_id: str, payload: dict) -> RoomEnvelope:
        data = self._post(f"/v1/games/{game_id}/rooms", data=payload)
        return RoomEnvelope.model_validate(data)

    def get_room(self, room_id: str) -> RoomEnvelope:
        data = self._get(f"/v1/rooms/{room_id}")
        return RoomEnvelope.model_validate(data)

    def put_room(self, room_id: str, payload: dict) -> RoomEnvelope:
        data = self._patch(f"/v1/rooms/{room_id}", data=payload)
        return RoomEnvelope.model_validate(data)

    def delete_room(self, room_id: str) -> dict | None:
        return self._delete(f"/v1/rooms/{room_id}")

    def post_claim(self, room_id: str, payload: dict) -> RoomClaimEnvelope:
        data = self._post(f"/v1/rooms/{room_id}/claims", data=payload)
        return RoomClaimEnvelope.model_validate(data)

    def update_claim(self, claim_id: str, payload: dict) -> RoomClaimEnvelope:
        data = self._patch(f"/v1/rooms/claims/{claim_id}", data=payload)
        return RoomClaimEnvelope.model_validate(data)

    def delete_claim(self, claim_id: str) -> dict | None:
        return self._delete(f"/v1/rooms/claims/{claim_id}")

    def create_pending_post(self, room_id: str, payload: dict) -> PendingPostEnvelope:
        data = self._post(f"/v1/rooms/{room_id}/pendings", data=payload)
        return PendingPostEnvelope.model_validate(data)

    def delete_pending_post(self, pending_post_id: str) -> dict | None:
        return self._delete(f"/v1/rooms/pendings/{pending_post_id}")
