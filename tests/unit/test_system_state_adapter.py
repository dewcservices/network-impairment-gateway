import unittest
from datetime import datetime

from app.adapters.system_state_adapter import SystemStateAdapter
from app.dtos.system_dtos import SystemStateDTO
from app.entities.models import SystemState


class TestSystemStateAdapter(unittest.TestCase):

    def test_SystemStateToDTO(self):
        # Arrange
        bearer_id = 1
        uplink_environment_id = 2
        downlink_environment_id = 2

        system_state = SystemState(
            id=1,
            bearer_id=bearer_id,
            uplink_environment_id=uplink_environment_id,
            downlink_environment_id=downlink_environment_id,
            updated_at=datetime.now(),
        )

        # Act
        result_dto = SystemStateAdapter.SystemStateToDTO(system_state)

        # Assert
        assert result_dto.bearer_id == bearer_id
        assert result_dto.uplink_environment_id == uplink_environment_id
        assert result_dto.downlink_environment_id == downlink_environment_id

    def test_DTOToSystemState(self):
        # Arrange
        bearer_id = 1
        uplink_environment_id = 2
        downlink_environment_id = 2
        system_state_dto = SystemStateDTO(
            bearer_id=bearer_id,
            uplink_environment_id=uplink_environment_id,
            downlink_environment_id=downlink_environment_id,
        )

        # Act
        result_system_state: SystemState = SystemStateAdapter.DTOToSystemState(
            system_state_dto
        )

        # Assert
        assert result_system_state.bearer_id == bearer_id
        assert result_system_state.uplink_environment_id == uplink_environment_id
        assert result_system_state.downlink_environment_id == downlink_environment_id

    def test_SystemStateToDTO_with_additional_fields(self):
        # Arrange
        bearer_id = 1
        uplink_environment_id = 2
        downlink_environment_id = 2
        system_state = SystemState(
            bearer_id=bearer_id,
            uplink_environment_id=uplink_environment_id,
            downlink_environment_id=downlink_environment_id,
        )
        system_state.updated_at = datetime.now()
        system_state.id = 1

        # Act
        result_dto = SystemStateAdapter.SystemStateToDTO(system_state)

        # Assert
        assert result_dto.bearer_id == bearer_id
        assert result_dto.uplink_environment_id == uplink_environment_id
        assert result_dto.downlink_environment_id == downlink_environment_id
