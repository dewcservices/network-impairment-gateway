from fastapi import APIRouter, Depends

from app.dependencies import get_setting_service
from app.dtos.response_dtos import ResponseDTO
from app.dtos.set_impairment_dtos import SetImpairmentDTO
from app.services.interfaces.isetting_service import ISettingService

router = APIRouter(prefix="/api/settings")


@router.post("/")
def set_impairment(
    payload: SetImpairmentDTO, service: ISettingService = Depends(get_setting_service)
) -> ResponseDTO:
    return service.set_impairment(payload)


@router.delete("/")
def delete_htb_netem_qdiscs(
    service: ISettingService = Depends(get_setting_service),
) -> ResponseDTO:
    return service.delete_htb_netem_qdiscs()
