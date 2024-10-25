import unittest

from app.adapters.hbt_adapter import HBTAdapter
from app.dtos.hbt_dtos import HBTDTO, HBTValueDTO
from app.entities.models import BearerLinkHBT


class TestHBTAdapter(unittest.TestCase):

    def setUp(self):
        self.kbit = "kbit"
        self.mbit = "mbit"
        self.gbit = "gbit"

    def test_ValueStrToHBTValueDTO_kbit(self):
        # arrange
        for i in range(1000):
            input = f"{i}{self.kbit}"
            # act
            result = HBTAdapter.ValueStrToHBTValueDTO(input)
            # assert
            assert result.value == i
            assert result.unit == self.kbit

    def test_ValueStrToHBTValueDTO_mbit(self):
        # arrange
        for i in range(1000):
            input = f"{i}{self.mbit}"
            # act
            result = HBTAdapter.ValueStrToHBTValueDTO(input)
            # assert
            assert result.value == i
            assert result.unit == self.mbit

    def test_ValueStrToHBTValueDTO_gbit(self):
        # arrange
        for i in range(1000):
            input = f"{i}{self.gbit}"
            # act
            result = HBTAdapter.ValueStrToHBTValueDTO(input)
            # assert
            assert result.value == i
            assert result.unit == self.gbit

    def test_DTOToBearerLinkHbt(self):
        # arrange
        ceil = HBTValueDTO(value=100, unit="mbit")
        rate = HBTValueDTO(value=50, unit="kbit")
        hbt = HBTDTO(ceil=ceil, rate=rate)
        # act
        result = HBTAdapter.DTOToBearerLinkHbt(hbt)
        # assert
        assert result.ceil == f"{hbt.ceil.value}{hbt.ceil.unit}"
        assert result.rate == f"{hbt.rate.value}{hbt.rate.unit}"

    def test_BearerLinkHbtToDTO(self):
        # arrange

        bearer_link_hbt = BearerLinkHBT()
        bearer_link_hbt.ceil = "55gbit"
        bearer_link_hbt.rate = "25mbit"
        # act
        result = HBTAdapter.BearerLinkHbtToDTO(bearer_link_hbt)
        # assert
        assert f"{result.ceil.value}{result.ceil.unit}" == bearer_link_hbt.ceil
        assert f"{result.rate.value}{result.rate.unit}" == bearer_link_hbt.rate
