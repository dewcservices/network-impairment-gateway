from app.dtos.system_dtos import SystemStateDTO
from app.entities.models import SystemState


class SystemStateAdapter:
    @staticmethod
    def SystemStateToDTO(system_state: SystemState) -> SystemStateDTO:
        return SystemStateDTO.model_validate(system_state)

    def DTOToSystemState(dto: SystemStateDTO) -> SystemState:
        # Convert Pydantic BearerDTO to SQLAlchemy Bearer using .dict() and **kwargs
        system_state_dict = dto.model_dump()
        # Create and return SQLAlchemy Bearer model
        return SystemState(**system_state_dict)
