import unittest
from unittest.mock import MagicMock

from app.adapters.bearer_adapter import BearerAdapter
from app.dtos.bearer_dtos import BearerDetailsDTO, BearerDTO
from app.entities.models import Bearer


class TestBearerAdapter(unittest.TestCase):

    def setUp(self):
        # Setup mock objects for Bearer, BearerDTO, and BearerDetailsDTO
        self.mock_bearer = MagicMock(spec=Bearer)
        self.mock_bearer_dto = MagicMock(spec=BearerDTO)
        self.mock_bearer_details_dto = MagicMock(spec=BearerDetailsDTO)

    def test_bearer_to_bearer_dto(self):
        # Mock the model_validate method to return a BearerDTO instance
        BearerDTO.model_validate = MagicMock(return_value=self.mock_bearer_dto)

        # Call the method to be tested
        result = BearerAdapter.BearerToBearerDTO(self.mock_bearer)

        # Assert that model_validate was called correctly
        BearerDTO.model_validate.assert_called_once_with(self.mock_bearer)

        # Assert that the result is the mock BearerDTO
        self.assertEqual(result, self.mock_bearer_dto)

    def test_bearer_to_bearer_details_dto(self):
        # Mock the model_validate method to return a BearerDetailsDTO instance
        BearerDetailsDTO.model_validate = MagicMock(
            return_value=self.mock_bearer_details_dto
        )

        # Call the method to be tested
        result = BearerAdapter.BearerToBearerDetailsDTO(self.mock_bearer)

        # Assert that model_validate was called correctly
        BearerDetailsDTO.model_validate.assert_called_once_with(self.mock_bearer)

        # Assert that the result is the mock BearerDetailsDTO
        self.assertEqual(result, self.mock_bearer_details_dto)

    def test_bearer_dto_to_bearer(self):
        # Mock the model_dump method to return a dictionary representation of BearerDTO
        self.mock_bearer_dto.model_dump = MagicMock(
            return_value={
                "id": 1,
                "name": "Test Bearer",
                "img": "http://example.com/image.png",
            }
        )

        # Call the method to be tested
        result = BearerAdapter.BearerDTOToBearer(self.mock_bearer_dto)

        # Assert that model_dump was called
        self.mock_bearer_dto.model_dump.assert_called_once()

        # Check if the img was converted to string and passed correctly
        self.assertEqual(result.img, "http://example.com/image.png")
        self.assertEqual(result.name, "Test Bearer")
        self.assertEqual(result.id, 1)


if __name__ == "__main__":
    unittest.main()
