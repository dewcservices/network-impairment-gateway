import unittest
from typing import List

from pydantic import HttpUrl

from app.adapters.bearer_adapter import BearerAdapter
from app.dtos.bearer_dtos import BearerDTO
from app.entities.models import Bearer


class TestBearerAdapter(unittest.TestCase):

    def setUp(self):
        self.id = 1
        self.title = "Test Bearer"
        self.description = "Test bearer description"
        self.img = "http://example.com/image.png"

    def test_BearerToBearerDetailsDTO(self):
        # arrange

        bearer = Bearer(
            id=self.id,
            active=True,
            description=self.description,
            title=self.title,
            img=self.img,
        )
        # act
        result = BearerAdapter.BearerToBearerDetailsDTO(bearer)
        # assert
        assert result.id == self.id
        assert result.title == self.title
        assert result.img == HttpUrl(self.img)
        assert result.description == self.description

    def test_BearersToBearerDetailsDTOs(self):
        # arrange
        count = [0, 1, 2]
        bearers: List[Bearer] = []
        for id in count:
            bearers.append(
                Bearer(
                    id=id,
                    active=True,
                    description=f"Test bearer {id + 1} description",
                    title=f"Test Bear {id + 1}",
                    img=f"http://example.com/{id + 1}.png",
                )
            )
        # act
        result = BearerAdapter.BearersToBearerDetailsDTOs(bearers=bearers)
        # assert
        for id in count:
            assert result[id].id == bearers[id].id
            assert result[id].title == bearers[id].title
            assert result[id].description == bearers[id].description
            assert result[id].img == HttpUrl(bearers[id].img)

    def test_BearerDTOToBearer(self):
        # arrange

        dto = BearerDTO(
            title=self.title,
            description=self.description,
            img=HttpUrl(self.img),
            links={
                "uplink": {
                    "hbt": {
                        "rate": {"value": 1000, "unit": "mbit"},
                        "ceil": {"value": 1200, "unit": "mbit"},
                    },
                    "netem": {
                        "delay": {"time": 50, "jitter": 10, "correlation": 80},
                        "loss": {"percentage": 1, "interval": 1000, "correlation": 50},
                    },
                },
                "downlink": {
                    "hbt": {
                        "rate": {"value": 800, "unit": "mbit"},
                        "ceil": {"value": 1000, "unit": "mbit"},
                    },
                    "netem": {
                        "delay": {"time": 70, "jitter": 15, "correlation": 60},
                        "loss": {"percentage": 2, "interval": 2000, "correlation": 40},
                    },
                },
            },
        )
        # act
        result = BearerAdapter.BearerDTOToBearer(dto)
        # assert
        assert result.title == self.title
        assert result.img == self.img
        assert result.description == self.description

    def test_BearerToBearerDTO(self):
        # arrange
        bearer = Bearer(
            id=self.id,
            active=True,
            description=self.description,
            title=self.title,
            img=self.img,
        )

        # act
        result = BearerAdapter.BearerToBearerDTO(bearer=bearer)
        # assert
        assert result.title == self.title
        assert result.img == HttpUrl(self.img)
        assert result.description == self.description
