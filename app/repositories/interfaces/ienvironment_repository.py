from abc import ABC, abstractmethod
from typing import List, Optional

from app.entities.models import Environment


class IEnvironmentRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[Environment]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Environment]:
        pass

    @abstractmethod
    def get_by_id_eager(self, id: int) -> Optional[Environment]:
        pass

    @abstractmethod
    def update(
        self,
        id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Optional[Environment]:
        pass

    @abstractmethod
    def create(
        self,
        title: str,
        description: str,
        netem_delay_time: int,
        netem_delay_jitter: int,
        delay_correlation: int,
        netem_loss_percentage: float,
        netem_loss_interval: int,
        netem_loss_correlation: int,
        netem_corrupt_percentage: float,
        netem_corrupt_correlation: int,
    ) -> Environment:
        pass

    @abstractmethod
    def delete(self, id: int):
        pass
