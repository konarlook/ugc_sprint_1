from aiokafka import AIOKafkaProducer
from pydantic import BaseModel

from .base import BaseBrokerProducer


class KafkaBrokerProducer(BaseBrokerProducer):
    def __init__(self, producer: AIOKafkaProducer):
        self.producer = producer

    async def produce(self, topic: str, message: BaseModel):
        print(1)
        print(topic, message.model_dump_json().encode("utf-8"))
        print(self.producer)
        await self.producer.start()
        await self.producer.send(
            topic=topic, value=message.model_dump_json().encode("utf-8")
        )
        await self.producer.stop()


# kafka_producer: KafkaBrokerProducer | None = KafkaBrokerProducer(
#     producer=AIOKafkaProducer(
#         bootstrap_servers="localhost:9094",
#         client_id='test'
#     )
# )


def get_kafka_producer() -> KafkaBrokerProducer:
    return KafkaBrokerProducer(
        producer=AIOKafkaProducer(
            bootstrap_servers="localhost:9094",
            client_id='test'
        )
    )
