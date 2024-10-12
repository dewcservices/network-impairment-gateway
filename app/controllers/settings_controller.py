from fastapi import APIRouter, Depends

from app.dependencies import get_setting_service
from app.services.interfaces.isetting_service import ISettingService

router = APIRouter(prefix="/api/settings")


@router.post("/")
async def create_htb_netem_qdiscs(
    payload, service: ISettingService = Depends(get_setting_service)
):

    return await service.create_htb_netem_qdiscs(payload)


@router.put("/bandwidth")
async def update_htb(payload, service: ISettingService = Depends(get_setting_service)):
    return await service.update_htb(payload)


@router.put("/netem")
async def update_netem(
    payload, service: ISettingService = Depends(get_setting_service)
):
    return await service.update_netem(payload)


@router.delete("/")
async def delete_htb_netem_qdiscs(
    service: ISettingService = Depends(get_setting_service),
):
    return await service.delete_htb_netem_qdiscs()
