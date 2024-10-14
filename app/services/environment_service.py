from typing import List

from app.dtos.environment_dtos import EnvironmentDTO
from app.dtos.response_dtos import ResponseDTO
from app.repositories.interfaces.ienvironment_repository import IEnvironmentRepository
from app.services.interfaces.ienvironment_service import IEnvironmentService


class EnvironmentService(IEnvironmentService):
    def __init__(self, repo: IEnvironmentRepository):
        self.repo = repo

    def get_all(self) -> List[EnvironmentDTO]:
        return List[EnvironmentDTO]

    def get(self, env_id: int) -> EnvironmentDTO:
        return EnvironmentDTO()

    def create(self, dto: EnvironmentDTO) -> ResponseDTO:
        return ResponseDTO(msg="environment create", isError=False)

    def update(self, env_id: int, dto: EnvironmentDTO) -> ResponseDTO:
        return ResponseDTO(msg="environment update", isError=False)

    def delete(self, env_id: int) -> ResponseDTO:
        return ResponseDTO(msg="environment delete", isError=False)
