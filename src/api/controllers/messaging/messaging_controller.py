from __future__ import annotations

from src.api.controllers.base_controller import BaseController
from src.api.models.messaging.messaging_model import (
    ConversationEnvelope,
    ConversationListEnvelope,
    MessageEnvelope,
    MessageListEnvelope,
)


class MessagingApi(BaseController):
    def get_conversations(
        self, skip: int | None = None, number: int | None = None, size: int | None = None
    ) -> ConversationListEnvelope:
        params = {}
        if skip is not None:
            params["skip"] = skip
        if number is not None:
            params["number"] = number
        if size is not None:
            params["size"] = size

        data = self._get("/v1/dialogues", params=params)
        return ConversationListEnvelope.model_validate(data)

    def get_visavi_conversation(self, login: str) -> ConversationEnvelope:
        data = self._get(f"/v1/dialogues/visavi/{login}")
        return ConversationEnvelope.model_validate(data)

    def get_conversation(self, id: str) -> ConversationEnvelope:
        data = self._get(f"/v1/dialogues/{id}")
        return ConversationEnvelope.model_validate(data)

    def get_messages(
        self, id: str, skip: int | None = None, number: int | None = None, size: int | None = None
    ) -> MessageListEnvelope:
        params = {}
        if skip is not None:
            params["skip"] = skip
        if number is not None:
            params["number"] = number
        if size is not None:
            params["size"] = size

        data = self._get(f"/v1/dialogues/{id}/messages", params=params)
        return MessageListEnvelope.model_validate(data)

    def post_message(self, id: str, message: dict) -> MessageListEnvelope:
        data = self._post(f"/v1/dialogues/{id}/messages", data=message)
        return MessageListEnvelope.model_validate(data)

    def delete_unread_messages(self, id: str) -> dict | None:
        return self._delete(f"/v1/dialogues/{id}/messages/unread")

    def get_message(self, id: str) -> MessageEnvelope:
        data = self._get(f"/v1/messages/{id}")
        return MessageEnvelope.model_validate(data)

    def delete_message(self, id: str) -> dict | None:
        return self._delete(f"/v1/messages/{id}")
