from abc import ABC, abstractmethod
from typing import List, Optional

from app.entities.models import Bearer


class IBearerRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[Bearer]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Bearer]:
        pass

    @abstractmethod
    def get_by_id_eager(self, id: int) -> Optional[Bearer]:
        pass

    @abstractmethod
    def update(
        self,
        id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        img: Optional[str] = None,
    ) -> Optional[Bearer]:
        pass

    @abstractmethod
    def create(self, title: str, description: str, img: Optional[str] = None) -> Bearer:
        pass

    # @abstractmethod
    # def create_bearer_link(
    #     self,
    #     id: int,
    #     link_type_id: int,
    #     hbt_rate: str,
    #     hbt_ceil: str,
    #     netem_delay_time: int,
    #     netem_delay_jitter: int,
    #     netem_loss_percentage: int,
    #     netem_loss_interval: int,
    #     netem_loss_correlation: int,
    # ) -> BearerLink:
    #     pass

    # @abstractmethod
    # def update_bearer_link(
    #     self,
    #     link_id: int,
    #     hbt_rate: Optional[str] = None,
    #     hbt_ceil: Optional[str] = None,
    #     netem_delay_time: Optional[int] = None,
    #     netem_delay_jitter: Optional[int] = None,
    #     netem_loss_percentage: Optional[int] = None,
    #     netem_loss_interval: Optional[int] = None,
    #     netem_loss_correlation: Optional[int] = None,
    # ) -> Optional[BearerLink]:
    #     pass

    @abstractmethod
    def delete(self, id: int):
        pass
