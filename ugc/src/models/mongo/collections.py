import datetime
from enum import IntEnum
from uuid import UUID

from beanie import Document, Indexed
from pydantic import Field


class ReviewScore(IntEnum):
    LIKE = 1
    DISLIKE = -1


class Review(Document):
    user_id: Indexed(str)
    movie_id: str
    score: int
    text: str
    is_delete: bool = Field(default=False)
    dt: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

    class Settings:
        name = 'review'
        use_state_management = True


class Bookmark(Document):
    user_id: Indexed(str)
    movie_id: str
    is_delete: bool = Field(default=False)
    dt: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

    class Settings:
        name = 'bookmark'
        use_state_management = True


class ReviewRating(Document):
    user_id: str
    review_id: Indexed(str)
    score: ReviewScore
    is_delete: bool = Field(default=False)
    dt: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

    class Settings:
        name = 'review_rating'
        use_state_management = True
