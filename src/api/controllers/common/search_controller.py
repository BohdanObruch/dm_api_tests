from src.api.controllers.base_controller import BaseController
from src.api.models.common.search_model import ObjectListEnvelope


class SearchApi(BaseController):
    def search(
        self, query: str, skip: int | None = None, number: int | None = None, size: int | None = None
    ) -> ObjectListEnvelope:
        params = {
            "query": query,
            "skip": skip,
            "number": number,
            "size": size,
        }
        # Remove None values from params to avoid sending them in the request
        params = {k: v for k, v in params.items() if v is not None}
        data = self._get("/v1/search", params=params)
        return ObjectListEnvelope.model_validate(data)
