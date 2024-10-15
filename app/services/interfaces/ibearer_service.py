from abc import ABC, abstractmethod
from typing import List

from app.dtos.bearer_dtos import BearerDetailsDTO, BearerDTO
from app.dtos.response_dtos import ResponseDTO


class IBearerService(ABC):
    @abstractmethod
    def get_all(self) -> List[BearerDetailsDTO]:
        pass

    @abstractmethod
    def get(self, earer_id: int) -> BearerDTO:
        pass

    @abstractmethod
    def create(self, dto: BearerDTO) -> ResponseDTO:
        pass

    @abstractmethod
    def update(self, bearer_id: int, dto: BearerDTO) -> ResponseDTO:
        pass

    @abstractmethod
    def delete(self, bearer_id: int) -> ResponseDTO:
        pass
