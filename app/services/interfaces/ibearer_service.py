from abc import ABC, abstractmethod


class IBearerService(ABC):
    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def get(self, earer_id: int) -> str:
        pass

    @abstractmethod
    async def create(self) -> str:
        pass

    @abstractmethod
    async def update(self, bearer_id: int) -> str:
        pass

    @abstractmethod
    async def delete(self, bearer_id: int) -> str:
        pass
