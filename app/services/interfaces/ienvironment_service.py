from abc import ABC, abstractmethod
from typing import List

from app.dtos.environment_dtos import Environment
from app.dtos.response_dtos import Response


class IEnvironmentService(ABC):
    @abstractmethod
    async def get_all(self) -> List[Environment]:
        pass

    @abstractmethod
    async def get(self, env_id: int) -> Environment:
        pass

    @abstractmethod
    async def create(self, dto: Environment) -> Response:
        pass

    @abstractmethod
    async def update(self, env_id: int, dto: Environment) -> Response:
        pass

    @abstractmethod
    async def delete(self, env_id: int) -> Response:
        pass
