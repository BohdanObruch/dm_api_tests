from __future__ import annotations

from src.api.controllers.base_controller import BaseController
from src.api.models.messaging.chat_model import ChatMessageEnvelope, ChatMessageListEnvelope


class ChatApi(BaseController):
    def get_chat_messages(
        self, skip: int | None = None, number: int | None = None, size: int | None = None
    ) -> ChatMessageListEnvelope:
        """
        Get chat messages.
        """
        params = {
            "skip": skip,
            "number": number,
            "size": size,
        }
        data = self._get("/v1/chat", params=params)
        return ChatMessageListEnvelope.model_validate(data)

    def post_chat_message(self, payload: dict) -> ChatMessageEnvelope:
        """
        Create new chat message.
        """
        data = self._post("/v1/chat", data=payload)
        return ChatMessageEnvelope.model_validate(data)

    def get_chat_message(self, id: str) -> ChatMessageEnvelope:
        """
        Get single chat message.
        """
        data = self._get(f"/v1/chat/{id}")
        return ChatMessageEnvelope.model_validate(data)
