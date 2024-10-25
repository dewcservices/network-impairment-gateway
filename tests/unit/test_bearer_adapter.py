import unittest
from typing import List

from pydantic import HttpUrl

from app.adapters.bearer_adapter import BearerAdapter, NetemAdapter
from app.constants import LinkTypes
from app.dtos.bearer_dtos import BearerDTO, BearerLinkDTO
from app.entities.models import Bearer, BearerLink, BearerLinkHBT, BearerLinkNetem


class TestBearerAdapter(unittest.TestCase):

    def setUp(self):
        self.id = 1
        self.title = "Test Bearer"
        self.description = "Test bearer description"
        self.img = "https://example.com/image.png"
        self.delay = NetemAdapter.DelayDTO(
            time=10,
            jitter=5,
            correlation=50,
        )
        self.loss = NetemAdapter.LossDTO(
            percentage=5,
            interval=100,
            correlation=15,
        )

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
                    img=f"https://example.com/{id + 1}.png",
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
        bearer.bearer_links = []
        uplink = self.create_bearer_link(
            link_type_id=int(LinkTypes.UPLINK.value),
            loss_percentage=5,
            loss_interval=100,
            loss_correlation=15,
            delay_time=10,
            delay_jitter=5,
            delay_correlation=50,
            ceil="25gbit",
            rate="10kbit",
        )
        downlink = self.create_bearer_link(
            link_type_id=int(LinkTypes.DOWNLINK.value),
            loss_percentage=5,
            loss_interval=100,
            loss_correlation=15,
            delay_time=10,
            delay_jitter=5,
            delay_correlation=50,
            ceil="25gbit",
            rate="10kbit",
        )

        bearer.bearer_links.append(uplink)
        bearer.bearer_links.append(downlink)

        # act
        result = BearerAdapter.BearerToBearerDTO(bearer=bearer)
        # assert
        assert result.title == self.title
        assert result.img == HttpUrl(self.img)
        assert result.description == self.description
        assert len(result.links) == 2
        self.assert_bearer_link(result.links.get(LinkTypes.UPLINK.name), uplink)
        self.assert_bearer_link(result.links.get(LinkTypes.DOWNLINK.name), downlink)

    def create_bearer_link(
        self,
        link_type_id: int,
        loss_percentage: int,
        loss_interval: int,
        loss_correlation: int,
        delay_time: int,
        delay_jitter: int,
        delay_correlation: int,
        ceil: str,
        rate: str,
    ) -> BearerLink:
        bearer_link_netem = BearerLinkNetem()
        bearer_link_netem.loss_percentage = loss_percentage
        bearer_link_netem.loss_interval = loss_interval
        bearer_link_netem.loss_correlation = loss_correlation
        bearer_link_netem.delay_time = delay_time
        bearer_link_netem.delay_jitter = delay_jitter
        bearer_link_netem.delay_correlation = delay_correlation
        bearer_link_hbt = BearerLinkHBT()
        bearer_link_hbt.ceil = ceil
        bearer_link_hbt.rate = rate
        bearer_link = BearerLink()
        bearer_link.link_type_id = link_type_id
        bearer_link.bearer_link_netem = bearer_link_netem
        bearer_link.bearer_link_hbt = bearer_link_hbt
        return bearer_link

    def assert_bearer_link(self, result: BearerLinkDTO, bearer_link: BearerLink):
        assert (
            result.netem.loss.percentage
            == bearer_link.bearer_link_netem.loss_percentage
        )
        assert result.netem.loss.interval == bearer_link.bearer_link_netem.loss_interval
        assert (
            result.netem.loss.correlation
            == bearer_link.bearer_link_netem.loss_correlation
        )
        assert result.netem.delay.time == bearer_link.bearer_link_netem.delay_time
        assert result.netem.delay.jitter == bearer_link.bearer_link_netem.delay_jitter
        assert (
            result.netem.delay.correlation
            == bearer_link.bearer_link_netem.delay_correlation
        )
        assert (
            f"{result.hbt.ceil.value}{result.hbt.ceil.unit}"
            == bearer_link.bearer_link_hbt.ceil
        )
        assert (
            f"{result.hbt.rate.value}{result.hbt.rate.unit}"
            == bearer_link.bearer_link_hbt.rate
        )

    def test_BearerLinkToBearerLinkDTO(self):
        # arrange
        bearer_link = self.create_bearer_link(
            link_type_id=LinkTypes.DOWNLINK.value,
            loss_percentage=5,
            loss_interval=100,
            loss_correlation=15,
            delay_time=10,
            delay_jitter=5,
            delay_correlation=50,
            ceil="25gbit",
            rate="10kbit",
        )

        # act
        result = BearerAdapter.BearerLinkToBearerLinkDTO(bearer_link)
        # assert
        self.assert_bearer_link(result, bearer_link)

    def test_BearerNetemToBearerNetemDTO(self):
        # arrange
        bearer_link_netem = BearerLinkNetem()
        bearer_link_netem.loss_percentage = 5
        bearer_link_netem.loss_interval = 100
        bearer_link_netem.loss_correlation = 15
        bearer_link_netem.delay_time = 10
        bearer_link_netem.delay_jitter = 5
        bearer_link_netem.delay_correlation = 50
        # act
        result = BearerAdapter.BearerNetemToBearerNetemDTO(
            bearer_link_netem=bearer_link_netem
        )
        # assert
        assert result.loss.percentage == bearer_link_netem.loss_percentage
        assert result.loss.interval == bearer_link_netem.loss_interval
        assert result.loss.correlation == bearer_link_netem.loss_correlation
        assert result.delay.time == bearer_link_netem.delay_time
        assert result.delay.jitter == bearer_link_netem.delay_jitter
        assert result.delay.correlation == bearer_link_netem.delay_correlation

    def test_BearerNetemToBearerHtbDTO(self):
        # arrange
        bearer_link_hbt = BearerLinkHBT()
        bearer_link_hbt.ceil = "25gbit"
        bearer_link_hbt.rate = "10kbit"
        # act
        result = BearerAdapter.BearerNetemToBearerHtbDTO(bearer_link_hbt)
        # assert
        assert f"{result.ceil.value}{result.ceil.unit}" == bearer_link_hbt.ceil
        assert f"{result.rate.value}{result.rate.unit}" == bearer_link_hbt.rate
