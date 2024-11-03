from abc import ABC, abstractmethod

from app.entities.models import SystemState


class ISystemStateRepository(ABC):
    @abstractmethod
    def get(self) -> SystemState:
        pass

    @abstractmethod
    def set(self, bearer_id: int, uplink_env_id: int, downlink_env_id: int) -> bool:
        pass
