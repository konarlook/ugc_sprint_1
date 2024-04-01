from functools import lru_cache

from broker.kafka import get_kafka_producer

from .base import BaseDataService
from models.click import Click

class ClickService(BaseDataService):
    """Service for clicks of users events"""

    def __init__(self, producer):
        super().__init__(producer=producer)

    async def produce(self, topicname: str, click: Click):
        return await self.producer.send(topicname=topicname, key="click", data=click)


@lru_cache()
def get_click_service():
    kafka_producer = get_kafka_producer()
    return ClickService(producer=kafka_producer)