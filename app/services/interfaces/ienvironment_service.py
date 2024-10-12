from abc import ABC, abstractmethod


class IEnvironmentService(ABC):
    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def get(self, env_id: int) -> str:
        pass

    @abstractmethod
    async def create(self) -> str:
        pass

    @abstractmethod
    async def update(self, env_id: int) -> str:
        pass

    @abstractmethod
    async def delete(self, env_id: int) -> str:
        pass
