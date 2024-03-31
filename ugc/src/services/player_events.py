import asyncio

from broker.kafka import get_kafka_producer
from models.player import PlayerProgress, PlayerSettingEvents
from .base import BaseDataService


class PlayerService(BaseDataService):
    """Service for view progress of players"""

    def __init__(self, producer):
        super().__init__(producer=producer)

    async def produce(self, topic_name: str, message_model: PlayerProgress | PlayerSettingEvents):
        print(0)
        await self.producer.produce(topic=topic_name, message=message_model)


def get_player_service():
    return PlayerService(producer=get_kafka_producer())
