import datetime
from enum import IntEnum
from uuid import UUID

from beanie import Document


class ReviewScore(IntEnum):
    LIKE = 1
    DISLIKE = -1


class Review(Document):
    user_id: UUID
    movie_id: UUID
    score: int
    text: str
    review_df: datetime.datetime

    class Settings:
        name = 'rewiew'
        use_state_management = True


class Bookmark(Document):
    user_id: UUID
    movie_id: UUID
    bookmark_df: datetime.datetime

    class Settings:
        name = 'bookmark'
        use_state_management = True


class ReviewRating(Document):
    user_id: UUID
    review_id: UUID
    score: ReviewScore
    review_rating_df: datetime.datetime

    class Settings:
        name = 'review_rating'
        use_state_management = True
