from abc import ABC, abstractmethod


class IProcessService(ABC):
    @abstractmethod
    def call(cmd: str):
        pass
