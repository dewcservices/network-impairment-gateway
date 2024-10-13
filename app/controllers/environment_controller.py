from typing import List

from fastapi import APIRouter, Depends

from app.dependencies import get_env_service
from app.dtos.environment_dtos import Environment
from app.dtos.response_dtos import Response
from app.services.interfaces.ienvironment_service import IEnvironmentService

router = APIRouter(prefix="/api/environments")


@router.get("/")
async def get_all(
    service: IEnvironmentService = Depends(get_env_service),
) -> List[Environment]:
    return await service.get_all()


@router.get("/{env_id}")
async def get(
    env_id: int, service: IEnvironmentService = Depends(get_env_service)
) -> Environment:
    return await service.get(env_id)


@router.post("/")
async def create(
    dto: Environment, service: IEnvironmentService = Depends(get_env_service)
) -> Response:
    return await service.create(dto)


@router.put("/{env_id}")
async def update(
    env_id: int,
    dto: Environment,
    service: IEnvironmentService = Depends(get_env_service),
) -> Response:
    return await service.update(env_id, dto)


@router.delete("/{env_id}")
async def delete(
    env_id: int, service: IEnvironmentService = Depends(get_env_service)
) -> Response:
    return await service.delete(env_id)
