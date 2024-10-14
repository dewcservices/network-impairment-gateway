from typing import List

from fastapi import APIRouter, Depends

from app.dependencies import get_env_service
from app.dtos.environment_dtos import EnvironmentDTO
from app.dtos.response_dtos import ResponseDTO
from app.services.interfaces.ienvironment_service import IEnvironmentService

router = APIRouter(prefix="/api/environments")


@router.get("/")
def get_all(
    service: IEnvironmentService = Depends(get_env_service),
) -> List[EnvironmentDTO]:
    return service.get_all()


@router.get("/{env_id}")
def get(
    env_id: int, service: IEnvironmentService = Depends(get_env_service)
) -> EnvironmentDTO:
    return service.get(env_id)


@router.post("/")
def create(
    dto: EnvironmentDTO, service: IEnvironmentService = Depends(get_env_service)
) -> ResponseDTO:
    return service.create(dto)


@router.put("/{env_id}")
def update(
    env_id: int,
    dto: EnvironmentDTO,
    service: IEnvironmentService = Depends(get_env_service),
) -> ResponseDTO:
    return service.update(env_id, dto)


@router.delete("/{env_id}")
def delete(
    env_id: int, service: IEnvironmentService = Depends(get_env_service)
) -> ResponseDTO:
    return service.delete(env_id)
