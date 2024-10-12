from abc import ABC, abstractmethod


class IEnvironmentService(ABC):
    @abstractmethod
    async def get_all():
        pass

    @abstractmethod
    async def get(env_id: int) -> str:
        pass

    @abstractmethod
    async def create() -> str:
        pass

    @abstractmethod
    async def update(env_id: int) -> str:
        pass

    @abstractmethod
    async def delete(env_id: int) -> str:
        pass
