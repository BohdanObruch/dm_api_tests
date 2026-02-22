from __future__ import annotations

from src.api.controllers.base_controller import BaseController
from src.api.models.community.review_model import ReviewEnvelope, ReviewListEnvelope


class ReviewApi(BaseController):
    def list(
        self,
        only_approved: bool | None = None,
        skip: int | None = None,
        number: int | None = None,
        size: int | None = None,
    ) -> ReviewListEnvelope:
        params = {
            "onlyApproved": only_approved,
            "skip": skip,
            "number": number,
            "size": size,
        }
        data = self._get("/v1/reviews", params=params)
        return ReviewListEnvelope.model_validate(data)

    def create(self, payload: dict) -> ReviewEnvelope:
        data = self._post("/v1/reviews", data=payload)
        return ReviewEnvelope.model_validate(data)

    def get_by_id(self, id: str) -> ReviewEnvelope:
        data = self._get(f"/v1/reviews/{id}")
        return ReviewEnvelope.model_validate(data)

    def update(self, id: str, payload: dict) -> ReviewEnvelope:
        data = self._patch(f"/v1/reviews/{id}", data=payload)
        return ReviewEnvelope.model_validate(data)

    def delete(self, id: str) -> None:
        self._delete(f"/v1/reviews/{id}")
