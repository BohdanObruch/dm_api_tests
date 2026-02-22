from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.api.models.messaging.common_model import BbParseMode, User
from src.api.models.shared.base_model import ResourceEnvelope, ResourceListEnvelope


class ChatBbText(BaseModel):
    model_config = ConfigDict(extra="allow")

    value: str | None = None
    parse_mode: BbParseMode | None = Field(default=None, alias="parseMode")


class ChatMessage(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    created: datetime | None = None
    author: User | None = None
    text: ChatBbText | None = None


ChatMessageEnvelope = ResourceEnvelope[ChatMessage]
ChatMessageListEnvelope = ResourceListEnvelope[ChatMessage]
