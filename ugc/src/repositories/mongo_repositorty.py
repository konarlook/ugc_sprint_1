from beanie import Document
from motor.motor_asyncio import AsyncIOMotorClient

from db.mongo import get_mongo_client
from repositories.base import BaseRepository


class MongoBeanieRepository(BaseRepository):
    def __init__(self, client: AsyncIOMotorClient, collection: str):
        self.mongo_collection = client['ugc'][collection]

    async def create(self, document: dict):
        await self.mongo_collection.insert_one(document)

    async def read(self, document: dict, skip: int = 0, limit: int = 100):
        response = self.mongo_collection.find(document).skip(skip).limit(limit)
        return await response.to_list(length=None)

    async def delete(self, document: dict):
        await self.mongo_collection.delete_one(document)


def get_mongo_repo(collection: str, client: AsyncIOMotorClient = get_mongo_client()):
    return MongoBeanieRepository(client=client, collection=collection)
