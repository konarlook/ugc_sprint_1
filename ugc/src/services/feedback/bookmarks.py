from functools import lru_cache

from fast_depends import inject, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from .base import BaseFeedbackService
from core.exceptions import EntityExistException, EntityNotExistException
from db.mongo import get_mongo_client
from schemas.response import BookmarkResponse


class BookmarkService(BaseFeedbackService):
    def __init__(self, client):
        super().__init__(
            client=client, collection="bookmark", response_class=BookmarkResponse
        )

    async def save_bookmark(self, document: dict):
        bookmark = await self.is_bookmark_exists(document=document)

        if not bookmark:
            await self.create(document=document)
            return

        if not self.is_delete_document(bookmark[0]):
            raise EntityExistException

        filter_data = {
            "user_id": document["user_id"],
            "movie_id": document["movie_id"],
        }
        document["is_delete"] = False

        await self.update(filter_data=filter_data, update_data=document)

    async def is_bookmark_exists(self, document: dict):
        doc = {
            "user_id": document["user_id"],
            "movie_id": document["movie_id"],
        }
        bookmark = await self.read(
            document=doc, sort_by="dt", skip=0, limit=1, sort_method=-1
        )
        return bookmark

    async def delete_bookmark(self, document: dict):
        bookmark = await self.is_bookmark_exists(document=document)

        if not bookmark or self.is_delete_document(bookmark[0]):
            raise EntityNotExistException

        filter_data = {
            "user_id": document["user_id"],
            "movie_id": document["movie_id"],
        }
        document["is_delete"] = True
        await self.update(filter_data=filter_data, update_data=document)
        return None


@lru_cache()
@inject
def get_bookmark_service(
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
) -> BookmarkService:
    return BookmarkService(mongo_client)
