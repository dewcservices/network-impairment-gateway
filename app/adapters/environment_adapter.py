from typing import List

from app.dtos.environment_dtos import EnvironmentDetailsDTO, EnvironmentDTO
from app.entities.models import Environment


class EnvironmentAdapter:

    @staticmethod
    def EnvironmentToEnvironmentDTO(Environment: Environment) -> EnvironmentDTO:
        return EnvironmentDTO.model_validate(Environment)

    @staticmethod
    def EnvironmentToEnvironmentDetailsDTO(
        Environment: Environment,
    ) -> EnvironmentDetailsDTO:
        return EnvironmentDetailsDTO.model_validate(Environment)

    @staticmethod
    def EnvironmentsToEnvironmentDetailsDTOs(
        Environments: List[Environment],
    ) -> List[EnvironmentDetailsDTO]:
        return [
            EnvironmentAdapter.EnvironmentToEnvironmentDetailsDTO(Environment)
            for Environment in Environments
        ]

    @staticmethod
    def EnvironmentDTOToEnvironment(dto: EnvironmentDTO) -> Environment:
        # Convert Pydantic EnvironmentDTO to SQLAlchemy Environment using .dict() and **kwargs
        Environment_dict = dto.model_dump()

        # Create and return SQLAlchemy Environment model
        return Environment(**Environment_dict)
