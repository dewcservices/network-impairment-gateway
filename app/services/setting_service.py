from app.dtos.response_dtos import Response
from app.dtos.set_impairment_dtos import SetImpairment
from app.services.interfaces.isetting_service import ISettingService


class SettingService(ISettingService):

    def __init__(self, interface: str):
        self.interface = interface

    async def set_impairment(self, payload: SetImpairment) -> Response:
        return Response(msg="Impairment set called", isError=False)

    async def delete_htb_netem_qdiscs(self) -> Response:
        return Response(msg="htb and netem qdisc added", isError=False)
