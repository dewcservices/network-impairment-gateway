from app.dtos.netem_dtos import NetemCorruptDTO, NetemDelayDTO, NetemLossDTO


class NetemAdapter:

    @staticmethod
    def DelayDTO(time: int, jitter: int, correlation: int) -> NetemDelayDTO:
        return NetemDelayDTO(time=time, jitter=jitter, correlation=correlation)

    @staticmethod
    def CorruptDTO(percentage: int, correlation: int) -> NetemCorruptDTO:
        return NetemCorruptDTO(percentage=percentage, correlation=correlation)

    @staticmethod
    def LossDTO(percentage: int, interval: int, correlation: int) -> NetemLossDTO:
        return NetemLossDTO(
            percentage=percentage, interval=interval, correlation=correlation
        )
