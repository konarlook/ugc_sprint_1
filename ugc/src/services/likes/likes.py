from functools import lru_cache

from db.mongo import get_mongo_client
from fast_depends import Depends, inject
from motor.motor_asyncio import AsyncIOMotorClient
from repositories.mongo_repository import MongoBeanieRepository


class LikeService(MongoBeanieRepository):
    def __init__(self, client):
        super().__init__(client=client, collection="like")

@lru_cache()
@inject
def get_like_service(
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
) -> LikeService:
    return LikeService(mongo_client)
