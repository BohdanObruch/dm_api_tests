from __future__ import annotations

from src.api.controllers.base_controller import BaseController
from src.api.models.community.poll_model import PollEnvelope, PollListEnvelope


class PollApi(BaseController):
    def list(
        self, only_active: bool = None, skip: int = None, number: int = None, size: int = None
    ) -> PollListEnvelope:
        params = {
            "onlyActive": only_active,
            "skip": skip,
            "number": number,
            "size": size,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = self._get("/v1/polls", params=params)
        return PollListEnvelope.model_validate(data)

    def create(self, payload: dict) -> PollEnvelope:
        data = self._post("/v1/polls", data=payload)
        return PollEnvelope.model_validate(data)

    def get(self, id: str) -> PollEnvelope:
        data = self._get(f"/v1/polls/{id}")
        return PollEnvelope.model_validate(data)

    def vote(self, id: str, option_id: str = None) -> PollEnvelope:
        params = {"optionId": option_id}
        params = {k: v for k, v in params.items() if v is not None}
        data = self._put(f"/v1/polls/{id}", params=params)
        return PollEnvelope.model_validate(data)
