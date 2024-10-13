from abc import ABC, abstractmethod
from typing import List

from app.dtos.bearer_dtos import Bearer
from app.dtos.response_dtos import Response


class IBearerService(ABC):
    @abstractmethod
    async def get_all(self) -> List[Bearer]:
        pass

    @abstractmethod
    async def get(self, earer_id: int) -> Bearer:
        pass

    @abstractmethod
    async def create(self, dto: Bearer) -> Response:
        pass

    @abstractmethod
    async def update(self, bearer_id: int, dto: Bearer) -> Response:
        pass

    @abstractmethod
    async def delete(self, bearer_id: int) -> Response:
        pass
