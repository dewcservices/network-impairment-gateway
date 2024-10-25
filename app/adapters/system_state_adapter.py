from app.adapters.dto_to_model_util import DtoToModelUtil
from app.dtos.system_dtos import SystemStateDTO
from app.entities.models import SystemState


class SystemStateAdapter:

    @staticmethod
    def SystemStateToDTO(system_state: SystemState) -> SystemStateDTO:

        return SystemStateDTO.model_validate(
            DtoToModelUtil.map_object_to_dto(system_state, SystemStateDTO)
        )

    def DTOToSystemState(dto: SystemStateDTO) -> SystemState:
        # Convert Pydantic BearerDTO to SQLAlchemy Bearer using .dict() and **kwargs
        system_state_dict = dto.model_dump()
        # Create and return SQLAlchemy Bearer model
        return SystemState(**system_state_dict)
