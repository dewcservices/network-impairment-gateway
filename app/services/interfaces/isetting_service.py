from abc import ABC, abstractmethod

from app.dtos.response_dtos import Response
from app.dtos.set_impairment_dtos import SetImpairment


class ISettingService(ABC):

    @abstractmethod
    async def set_impairment(self, payload: SetImpairment) -> Response:
        pass

    @abstractmethod
    async def delete_htb_netem_qdiscs(self) -> Response:
        pass
