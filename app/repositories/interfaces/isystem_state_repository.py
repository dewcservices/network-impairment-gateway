from abc import ABC, abstractmethod

from app.entities.models import SystemState


class ISystemStateRepository(ABC):
    @abstractmethod
    def get() -> SystemState:
        pass

    @abstractmethod
    def set(bearer_id: int, env_id: int) -> bool:
        pass
