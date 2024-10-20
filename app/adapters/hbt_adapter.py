from app.dtos.hbt_dtos import HBTDTO, HBTValueDTO
from app.entities.models import BearerLinkHBT


class HBTAdapter:

    @staticmethod
    def BearerLinkHbtToDTO(hbt: BearerLinkHBT) -> HBTDTO:
        dto = HBTDTO()
        dto.ceil = HBTValueDTO(value=hbt.ceil, unit=hbt.ceil)
        dto.rate = HBTValueDTO(value=hbt.rate, unit=hbt.rate)
        return dto

    @staticmethod
    def DTOToBearerLinkHbt(dto: HBTDTO) -> BearerLinkHBT:
        hbt = BearerLinkHBT()
        hbt.ceil = f"{dto.ceil.value}{dto.ceil.unit}"
        hbt.rate = f"{dto.rate.value}{dto.rate.unit}"
        return hbt
