from .base import BaseDataService


class ClickService(BaseDataService):
    """Service for clicks of users events"""

    def __init__(self, producer):
        super().__init__(producer=producer)

    async def produce(self):
        pass
