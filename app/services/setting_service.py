from app.dtos.response_dtos import ResponseDTO
from app.dtos.set_impairment_dtos import SetImpairmentDTO
from app.services.interfaces.isetting_service import ISettingService


class SettingService(ISettingService):

    def __init__(self, interface: str):
        self.interface = interface

    async def set_impairment(self, payload: SetImpairmentDTO) -> ResponseDTO:
        return ResponseDTO(msg="Impairment set called", isError=False)

    async def delete_htb_netem_qdiscs(self) -> ResponseDTO:
        return ResponseDTO(msg="htb and netem qdisc added", isError=False)
