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
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

    class Settings:
        name = 'review'
        use_state_management = True


class Bookmark(Document):
    user_id: Indexed(str)
    movie_id: UUID
    dt: datetime.datetime

    class Settings:
        name = 'bookmark'
        use_state_management = True


class ReviewRating(Document):
    user_id: str
    review_id: Indexed(str)
    score: ReviewScore
    dt: datetime.datetime

    class Settings:
        name = 'review_rating'
        use_state_management = True
