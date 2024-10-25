from abc import ABC, abstractmethod


class IProcessService(ABC):
    @abstractmethod
    def run(self, cmd: str):
        pass
