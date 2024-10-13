from typing import List

from fastapi import APIRouter, Depends

from app.dependencies import get_bearer_service
from app.dtos.bearer_dtos import Bearer
from app.dtos.response_dtos import Response
from app.services.interfaces.ibearer_service import IBearerService

router = APIRouter(prefix="/api/bearers")


@router.get("/")
async def get_all(
    service: IBearerService = Depends(get_bearer_service),
) -> List[Bearer]:
    return await service.get_all()


@router.get("/{bearer_id}")
async def get(
    bearer_id: int, service: IBearerService = Depends(get_bearer_service)
) -> Bearer:
    return await service.get(bearer_id)


@router.post("/")
async def create(
    dto: Bearer, service: IBearerService = Depends(get_bearer_service)
) -> Response:
    return await service.create(dto)


@router.put("/{bearer_id}")
async def update(
    bearer_id: int, dto: Bearer, service: IBearerService = Depends(get_bearer_service)
) -> Response:
    return await service.update(bearer_id, dto)


@router.delete("/{bearer_id}")
async def delete(
    bearer_id: int, service: IBearerService = Depends(get_bearer_service)
) -> Response:
    return await service.delete(bearer_id)
