from typing import List

from fastapi import APIRouter, Depends

from app.dependencies import get_bearer_service
from app.dtos.bearer_dtos import BearerDetailsDTO, BearerDTO
from app.dtos.response_dtos import ResponseDTO
from app.services.interfaces.ibearer_service import IBearerService

router = APIRouter(prefix="/api/bearers")


@router.get("/")
def get_all(
    service: IBearerService = Depends(get_bearer_service),
) -> List[BearerDetailsDTO]:
    temp = service.get_all()
    print(temp)
    return temp


@router.get("/{bearer_id}")
def get(
    bearer_id: int, service: IBearerService = Depends(get_bearer_service)
) -> BearerDTO:
    return service.get(bearer_id)


@router.post("/")
def create(
    dto: BearerDTO, service: IBearerService = Depends(get_bearer_service)
) -> ResponseDTO:
    return service.create(dto)


@router.put("/{bearer_id}")
def update(
    bearer_id: int,
    dto: BearerDTO,
    service: IBearerService = Depends(get_bearer_service),
) -> ResponseDTO:
    return service.update(bearer_id, dto)


@router.delete("/{bearer_id}")
def delete(
    bearer_id: int, service: IBearerService = Depends(get_bearer_service)
) -> ResponseDTO:
    return service.delete(bearer_id)
