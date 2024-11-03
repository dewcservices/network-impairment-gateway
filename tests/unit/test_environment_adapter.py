import unittest
from typing import List

from app.adapters.environment_adapter import EnvironmentAdapter
from app.entities.models import Environment


class TestEnvironmentAdapter(unittest.TestCase):

    def setUp(self):
        self.id = 1
        self.title = "Test Environment"
        self.description = "Test environment description"

    def test_EnvironmentToEnvironmentDTO(self):
        # arrange
        env = Environment(
            id=self.id,
            title=self.title,
            description=self.description,
            active=True,
            environment_netem=[],
        )
        # act
        result = EnvironmentAdapter.EnvironmentToEnvironmentDTO(env)
        # assert
        assert result.title == self.title
        assert result.description == self.description

    def test_EnvironmentToEnvironmentDetailsDTO(self):
        # arrange
        env = Environment(
            id=self.id,
            title=self.title,
            description=self.description,
            active=True,
        )
        # act
        result = EnvironmentAdapter.EnvironmentToEnvironmentDetailsDTO(env)
        # assert
        assert result.id == self.id
        assert result.title == self.title
        assert result.description == self.description
        pass

    def test_EnvironmentsToEnvironmentDetailsDTOs(self):
        # arrange
        count = [0, 1, 2]
        envs: List[Environment] = []
        for id in count:
            envs.append(
                Environment(
                    id=id,
                    title=f"Test Environment {id}",
                    description=f"Test environment {id}",
                    active=True,
                )
            )

        # act
        # assert
        pass

    def test_EnvironmentDTOToEnvironment(self):
        # arrange
        # act
        # assert
        pass
