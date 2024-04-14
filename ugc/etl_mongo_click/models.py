from uuid import UUID
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class Review(BaseModel):
    user_id: UUID = Field(comment="Идентификатор пользователя")
    movie_id: UUID = Field(comment="Идентификатор фильма")
    score: int = Field(comment="Полезность отзыва")
    text: str = Field(comment="Тест отзыва")
    is_delete: bool = Field(comment="Пометка об удалении")
    dt: datetime = Field(comment='Дата события', alias='event_dt')


class Bookmark(BaseModel):
    user_id: UUID = Field(comment="Идентификатор пользователя")
    movie_id: UUID = Field(comment="Идентификатор фильма")
    is_delete: bool = Field(comment="Пометка об удалении")
    dt: datetime = Field(comment='Дата события', alias='event_dt')


class ReviewRating(BaseModel):
    user_id: UUID = Field(comment="Идентификатор пользователя")
    review_id: UUID = Field(comment="Идентификатор отзыва")
    score: int = Field(comment="Полезность отзыва")
    is_delete: bool = Field(comment="Пометка об удалении")
    dt: datetime = Field(comment='Дата события', alias='event_dt')
