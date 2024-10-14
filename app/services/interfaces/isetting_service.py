from abc import ABC, abstractmethod

from app.dtos.response_dtos import ResponseDTO
from app.dtos.set_impairment_dtos import SetImpairmentDTO


class ISettingService(ABC):

    @abstractmethod
    def set_impairment(self, payload: SetImpairmentDTO) -> ResponseDTO:
        pass

    @abstractmethod
    def delete_htb_netem_qdiscs(self) -> ResponseDTO:
        pass
