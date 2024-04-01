from broker.base import BaseBrokerProducer
from .base import BaseDataService


class ClickService(BaseDataService):
    """Service for clicks of users events"""

    def __init__(self, producer: BaseBrokerProducer):
        super().__init__(producer=producer)

    async def send_message(self):
        pass
