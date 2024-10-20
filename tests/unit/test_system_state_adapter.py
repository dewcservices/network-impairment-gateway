import unittest
from datetime import datetime

from app.adapters.system_state_adapter import SystemStateAdapter
from app.dtos.system_dtos import SystemStateDTO
from app.entities.models import SystemState


class TestSystemStateAdapter(unittest.TestCase):

    def test_SystemStateToDTO(self):
        # Arrange
        bearer_id = 1
        environment_id = 2

        system_state = SystemState(
            id=1,
            bearer_id=bearer_id,
            environment_id=environment_id,
            updated_at=datetime.now(),
        )

        # Act
        result_dto = SystemStateAdapter.SystemStateToDTO(system_state)

        # Assert
        assert result_dto.bearer_id == bearer_id
        assert result_dto.environment_id == environment_id

    def test_DTOToSystemState(self):
        # Arrange
        bearer_id = 1
        environment_id = 2
        system_state_dto = SystemStateDTO(
            bearer_id=bearer_id, environment_id=environment_id
        )

        # Act
        result_system_state = SystemStateAdapter.DTOToSystemState(system_state_dto)

        # Assert
        assert result_system_state.bearer_id == bearer_id
        assert result_system_state.environment_id == environment_id

    def test_SystemStateToDTO_with_additional_fields(self):
        # Arrange
        bearer_id = 1
        environment_id = 2
        system_state = SystemState(bearer_id=bearer_id, environment_id=environment_id)
        system_state.updated_at = datetime.now()
        system_state.id = 1

        # Act
        result_dto = SystemStateAdapter.SystemStateToDTO(system_state)

        # Assert
        assert result_dto.bearer_id == bearer_id
        assert result_dto.environment_id == environment_id
