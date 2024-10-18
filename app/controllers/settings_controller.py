from fastapi import APIRouter, Depends

from app.dependencies import get_setting_service
from app.dtos.response_dtos import ResponseDTO
from app.dtos.system_dtos import SystemStateDTO
from app.services.interfaces.isystem_state_service import ISystemStateService

router = APIRouter(prefix="/api/settings")


@router.get("/")
def get(service: ISystemStateService = Depends(get_setting_service)) -> SystemStateDTO:
    return service.get()


@router.post("/")
def set_impairment(
    payload: SystemStateDTO, service: ISystemStateService = Depends(get_setting_service)
) -> ResponseDTO:
    return service.set_impairment(payload)


@router.delete("/")
def delete_htb_netem_qdiscs(
    service: ISystemStateService = Depends(get_setting_service),
) -> ResponseDTO:
    return service.delete_htb_netem_qdiscs()
