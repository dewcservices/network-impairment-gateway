from abc import ABC, abstractmethod
from typing import List

from app.dtos.environment_dtos import EnvironmentDTO
from app.dtos.response_dtos import ResponseDTO


class IEnvironmentService(ABC):
    @abstractmethod
    def get_all(self) -> List[EnvironmentDTO]:
        pass

    @abstractmethod
    def get(self, env_id: int) -> EnvironmentDTO:
        pass

    @abstractmethod
    def create(self, dto: EnvironmentDTO) -> ResponseDTO:
        pass

    @abstractmethod
    def update(self, env_id: int, dto: EnvironmentDTO) -> ResponseDTO:
        pass

    @abstractmethod
    def delete(self, env_id: int) -> ResponseDTO:
        pass
