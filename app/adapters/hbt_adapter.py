from app.dtos.hbt_dtos import HBTDTO
from app.entities.models import BearerLinkHBT


class HBTAdapter:

    @staticmethod
    def BearerLinkHbtToDTO(hbt: BearerLinkHBT) -> HBTDTO:
        return HBTDTO.model_validate(hbt)

    @staticmethod
    def DTOToBearerLinkHbt(dto: HBTDTO) -> BearerLinkHBT:
        hbt_dict = dto.model_dump()
        return BearerLinkHBT(**hbt_dict)
