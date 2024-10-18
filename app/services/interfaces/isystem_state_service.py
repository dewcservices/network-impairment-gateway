from abc import ABC, abstractmethod

from app.dtos.response_dtos import ResponseDTO
from app.dtos.system_dtos import SystemStateDTO


class ISystemStateService(ABC):

    @abstractmethod
    def get(self) -> SystemStateDTO:
        pass

    @abstractmethod
    def set_impairment(self, payload: SystemStateDTO) -> ResponseDTO:
        pass

    @abstractmethod
    def delete_htb_netem_qdiscs(self) -> ResponseDTO:
        pass
