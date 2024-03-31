from aiokafka import AIOKafkaProducer
from .base import BaseBrokerProducer


class KafkaBrokerProducer(BaseBrokerProducer):
    def __init__(self, producer: AIOKafkaProducer):
        self.producer = producer

    async def produce(self, topic: str, key: str, data):
        await self.producer.send(
            topic=topic, key=key.encode("utf-8"), value=data.json().encode("utf-8")
        )


kafka_producer: KafkaBrokerProducer | None = None


def get_kafka_producer() -> KafkaBrokerProducer:
    return kafka_producer
