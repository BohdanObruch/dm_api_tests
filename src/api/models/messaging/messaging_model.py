from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.api.models.messaging.common_model import CommonBbText, User
from src.api.models.shared.base_model import ResourceEnvelope, ResourceListEnvelope


class Message(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str = Field(description="Identifier", json_schema_extra={"format": "uuid"})
    created: datetime = Field(description="Creating moment", json_schema_extra={"format": "date-time"})
    author: User = Field()
    text: CommonBbText = Field()


class Conversation(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str = Field(description="Identifier", json_schema_extra={"format": "uuid"})
    name: str | None = Field(default=None, description="Conversation name")
    participants: list[User] | None = Field(default=None, description="Conversation participants")
    last_message: Message | None = Field(default=None, alias="lastMessage")
    unread_messages_count: int = Field(
        description="Number of unread conversation messages",
        json_schema_extra={"format": "int32"},
    )


ConversationEnvelope = ResourceEnvelope[Conversation]
ConversationListEnvelope = ResourceListEnvelope[Conversation]
MessageEnvelope = ResourceEnvelope[Message]
MessageListEnvelope = ResourceListEnvelope[Message]
