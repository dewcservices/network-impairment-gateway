from abc import ABC, abstractmethod


class IBearerService(ABC):
    @abstractmethod
    async def get_all():
        pass

    @abstractmethod
    async def get(bearer_id: int) -> str:
        pass

    @abstractmethod
    async def create() -> str:
        pass

    @abstractmethod
    async def update(bearer_id: int) -> str:
        pass

    @abstractmethod
    async def delete(bearer_id: int) -> str:
        pass
