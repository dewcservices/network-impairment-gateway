from fastapi import APIRouter, Depends

from app.dependencies import get_env_service
from app.services.interfaces.ienvironment_service import IEnvironmentService

router = APIRouter(prefix="/api/environments")


@router.get("/")
async def get_all(service: IEnvironmentService = Depends(get_env_service)):
    return await service.get_all()


@router.get("/{env_id}")
async def get(
    env_id: int, service: IEnvironmentService = Depends(get_env_service)
) -> str:
    return await service.get(env_id)


@router.post("/")
async def create(service: IEnvironmentService = Depends(get_env_service)) -> str:
    return await service.create()


@router.put("/{env_id}")
async def update(
    env_id: int, service: IEnvironmentService = Depends(get_env_service)
) -> str:
    return await service.update(env_id)


@router.delete("/{env_id}")
async def delete(
    env_id: int, service: IEnvironmentService = Depends(get_env_service)
) -> str:
    return await service.delete(env_id)
