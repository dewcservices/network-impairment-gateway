from abc import ABC, abstractmethod


class IProcessService(ABC):
    @abstractmethod
    def call(self, cmd: str):
        pass
