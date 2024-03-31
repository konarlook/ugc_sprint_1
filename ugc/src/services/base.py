from abc import ABC, abstractmethod


class BaseDataService(ABC):
    def __init__(self, producer):
        self.producer = producer

    @abstractmethod
    def produce(self, *args, **kwargs):
        pass
