import math
from abc import ABC

from schemas.base import Page
from repositories.mongo_repositorty import MongoBeanieRepository


class BaseFeedbackService(ABC, MongoBeanieRepository):
    def __init__(self, client, collection, response_class):
        super().__init__(client=client, collection=collection)
        self.response_class = response_class

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

    async def get_with_pagination(self, document: dict, pagination_settings: dict):
        page_size, page_number, total_pages = await self.get_pagination_settings(
            document=document, pagination_settings=pagination_settings
        )

        res = await self.read(
            document=document,
            skip=(page_number - 1) * page_size,
            limit=page_size * page_number,
        )

        list_bookmarks = [self.response_class(**doc) for doc in res]

        response = Page(
            response=list_bookmarks,
            page=page_number,
            page_size=page_size,
            total_pages=total_pages,
        )

        return response
