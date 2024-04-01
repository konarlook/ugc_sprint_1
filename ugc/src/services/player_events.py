from .base import BaseDataService


class PlayerService(BaseDataService):
    """Service for view progress of players"""

    def __init__(self, producer):
        super().__init__(producer=producer)

    async def produce(self):
        pass
