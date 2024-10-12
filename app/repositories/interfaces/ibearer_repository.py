from abc import ABC, abstractmethod
from typing import List


class IBearerRepository(ABC):

    @abstractmethod
    async def create(self, bearer: any) -> any:
        pass

    @abstractmethod
    async def get_all(self) -> List[any]:
        pass

    @abstractmethod
    async def get(self, id: int) -> any:
        pass

    @abstractmethod
    async def update(self, bearer: any, id: int) -> any:
        pass

    @abstractmethod
    async def delete(self, id: int):
        pass
