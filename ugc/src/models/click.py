import datetime
from enum import Enum
from uuid import UUID

from pydantic import Field

from models.base import KafkaModelConfig


class ClickEvent(KafkaModelConfig):
    user_id: UUID = Field(description="UUID пользователя")
    movie_id: UUID = Field(description="UUID произведения")
    current_url: str = Field(default_factory=datetime.datetime.utcnow, description="Время события")
    destination_url: str = Field(description="Тип события")
