import unittest

from app.adapters.netem_adapter import NetemAdapter


class TestNetemAdapter(unittest.TestCase):
    def test_DelayDTO(self):
        # arrange
        time = 10
        jitter = 5
        correlation = 50
        # act
        result = NetemAdapter.DelayDTO(
            time=time, jitter=jitter, correlation=correlation
        )
        # assert
        assert result.time == time
        assert result.jitter == jitter
        assert result.correlation == correlation
        pass

    def test_CorruptDTO(self):
        # arrange
        percentage = 25
        correlation = 10

        # act
        result = NetemAdapter.CorruptDTO(percentage=percentage, correlation=correlation)

        # assert
        assert result.percentage == percentage
        assert result.correlation == correlation

    def test_LossDTO(self):
        # arrange
        percentage = 5
        interval = 100
        correlation = 15

        # act
        result = NetemAdapter.LossDTO(
            percentage=percentage, interval=interval, correlation=correlation
        )

        # assert
        assert result.percentage == percentage
        assert result.interval == interval
        assert result.correlation == correlation
