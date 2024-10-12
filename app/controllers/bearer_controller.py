from fastapi import APIRouter, Depends

from app.services.interfaces.ibearer_service import IBearerService

router = APIRouter(prefix="/api/bearers")


@router.get("/")
async def get_all(service: IBearerService = Depends()):
    return await service.get_all()


@router.get("/{bearer_id}")
async def get(bearer_id: int, service: IBearerService = Depends()) -> str:
    return await service.get(bearer_id)


@router.post("/")
async def create(service: IBearerService = Depends()) -> str:
    return await service.create()


@router.put("/{bearer_id}")
async def update(bearer_id: int, service: IBearerService = Depends()) -> str:
    return await service.update(bearer_id)


@router.delete("/{bearer_id}")
async def delete(bearer_id: int, service: IBearerService = Depends()) -> str:
    return await service.delete(bearer_id)
