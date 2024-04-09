from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import settings
from db.mongo import get_mongo_client
from helpers import logger
from models.mongo.collections import Review, ReviewRating, Bookmark

mongo_logger = logger.UGCLogger()


class MongoDBInit:
    def __init__(self, mongodb_client: AsyncIOMotorClient):
        self.client = mongodb_client

    async def create_collections(self):
        self.client.db_name = settings.mongodb.mongodb_db_name
        await init_beanie(database=self.client.db_name, document_models=[Review, Bookmark, ReviewRating])


def get_mongodb_init() -> MongoDBInit:
    return MongoDBInit(mongodb_client=get_mongo_client())
