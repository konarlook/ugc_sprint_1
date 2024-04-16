import math
from functools import lru_cache

from fast_depends import inject, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from core.exceptions import EntityExistException, EntityNotExistException
from db.mongo import get_mongo_client
from repositories.mongo_repositorty import MongoBeanieRepository
from schemas.base import Page
from schemas.response import BookmarkResponse


class BookmarkService(MongoBeanieRepository):
    def __init__(self, client):
        super().__init__(client=client, collection="bookmark")

    @staticmethod
    def is_delete_document(document: dict):
        return document.get("is_delete")

    async def get_pagination_settings(self, document: dict, pagination_settings: dict):
        if "page_size" not in pagination_settings:
            page_size = 50
        else:
            page_size = pagination_settings["page_size"]
        if "page_number" not in pagination_settings:
            page_number = 1
        else:
            page_number = pagination_settings["page_number"]

        total_documents = await self.count(document=document)
        total_pages = math.ceil(total_documents / page_size)

        return page_size, page_number, total_pages

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
        bookmark = await self.read(document=doc, sort_by="dt", skip=0, limit=1, sort_method=-1)
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

        return

    async def get_bookmarks(self, document: dict, pagination_settings: dict):
        page_size, page_number, total_pages = await self.get_pagination_settings(
            document=document,
            pagination_settings=pagination_settings
        )

        res = await self.read(
            document=document,
            skip=(page_number - 1) * page_size,
            limit=page_size * page_number,
        )

        list_bookmarks = [BookmarkResponse(**doc) for doc in res]

        response = Page(
            response=list_bookmarks,
            page=page_number,
            page_size=page_size,
            total_pages=total_pages,
        )

        return response


@lru_cache()
@inject
def get_bookmark_service(
        mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
) -> BookmarkService:
    return BookmarkService(mongo_client)
