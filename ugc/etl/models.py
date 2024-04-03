import logging

from uuid import UUID
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, validator


class EventsNames(Enum):
    change_resolution_to_480 = "change_resolution_to_480"
    change_resolution_to_720 = "change_resolution_to_720"
    change_resolution_to_1080 = "change_resolution_to_1080"
    change_resolution_to_1440 = "change_resolution_to_1440"
    change_resolution_to_2160 = "change_resolution_to_2160"


class PlayerProgressEventSchema(BaseModel):
    user_id: UUID = Field(comment="Идентификатор пользователя")
    movie_id: UUID = Field(comment="Идентификатор фильма")
    event_dt: datetime = Field(comment="Прогресс просмотра фильма")
    view_progress: int = Field(comment="События в плеере")
    movie_duration: int = Field(comment="Длительность фильма")

    @validator('view_progress', 'movie_duration')
    def compare_duration_and_view(self):
        if self.view_progress > self.movie_duration:
            logging.error(
                'View_progress is larger than movie_duration.'
                f'{self.user_id},{self.movie_id},'
                f'{self.event_dt},{self.view_progress},{self.movie_duration}')
        return None


class PlayerSettingsEventSchema(BaseModel):
    user_id: UUID = Field(comment="Идентификатор пользователя")
    movie_id: UUID = Field(comment="Идентификатор фильма")
    event_dt: datetime = Field(comment="Время события")
    event_type: EventsNames = Field(comment="События в плеере")


class ClickEventSchema(BaseModel):
    user_id: UUID = Field(comment="Идентификатор пользователя")
    current_url: str = Field(comment="URL текущей страницы")
    destination_url: str = Field(comment="URL запроса")
