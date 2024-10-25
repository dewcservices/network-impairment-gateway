from typing import List

from app.adapters.dto_to_model_util import DtoToModelUtil
from app.adapters.netem_adapter import NetemAdapter
from app.dtos.environment_dtos import (
    EnvironmentDetailsDTO,
    EnvironmentDTO,
    EnvironmentNetemDTO,
)
from app.entities.models import Environment, EnvironmentNetem


class EnvironmentAdapter:

    @staticmethod
    def EnvironmentToEnvironmentDTO(environment: Environment) -> EnvironmentDTO:
        # TODO Need to fix Environment Database so netem is a one to one relationship
        dto = EnvironmentDTO(
            title=environment.title,
            description=environment.description,
            netem=EnvironmentAdapter.EnvironmentNetemToEnvironmentNetemDTO(
                environment.environment_netem[0]
            ),
        )
        return dto

    @staticmethod
    def EnvironmentToEnvironmentDetailsDTO(
        environment: Environment,
    ) -> EnvironmentDetailsDTO:
        return EnvironmentDetailsDTO.model_validate(
            DtoToModelUtil.map_object_to_dto(environment, EnvironmentDetailsDTO)
        )

    @staticmethod
    def EnvironmentsToEnvironmentDetailsDTOs(
        environments: List[Environment],
    ) -> List[EnvironmentDetailsDTO]:
        return [
            EnvironmentAdapter.EnvironmentToEnvironmentDetailsDTO(environment)
            for environment in environments
        ]

    @staticmethod
    def EnvironmentNetemToEnvironmentNetemDTO(
        env_netem: EnvironmentNetem,
    ) -> EnvironmentNetemDTO:
        delay = NetemAdapter.DelayDTO(
            time=env_netem.delay_time,
            jitter=env_netem.delay_jitter,
            correlation=env_netem.delay_correlation,
        )
        loss = NetemAdapter.LossDTO(
            percentage=env_netem.loss_percentage,
            interval=env_netem.loss_interval,
            correlation=env_netem.loss_correlation,
        )

        corrupt = NetemAdapter.CorruptDTO(
            percentage=env_netem.corrupt_percentage,
            correlation=env_netem.corrupt_correlation,
        )

        return EnvironmentNetemDTO(delay=delay, loss=loss, corrupt=corrupt)

    @staticmethod
    def EnvironmentDTOToEnvironment(dto: EnvironmentDTO) -> Environment:
        # Convert Pydantic EnvironmentDTO to SQLAlchemy Environment using .dict() and **kwargs
        environment_dict = dto.model_dump()

        # Create and return SQLAlchemy Environment model
        return Environment(**environment_dict)
