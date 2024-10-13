from fastapi import APIRouter, Depends

from app.dependencies import get_setting_service
from app.dtos.response_dtos import Response
from app.dtos.set_impairment_dtos import SetImpairment
from app.services.interfaces.isetting_service import ISettingService

router = APIRouter(prefix="/api/settings")


@router.post("/")
async def set_impairment(
    payload: SetImpairment, service: ISettingService = Depends(get_setting_service)
) -> Response:
    return await service.set_impairment(payload)


@router.delete("/")
async def delete_htb_netem_qdiscs(
    service: ISettingService = Depends(get_setting_service),
) -> Response:
    return await service.delete_htb_netem_qdiscs()
