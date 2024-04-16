from uuid import UUID

from schemas.base import BaseSchema


class BookmarkResponse(BaseSchema):
    user_id: UUID
    movie_id: UUID
