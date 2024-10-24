import re

from app.dtos.hbt_dtos import HBTDTO, HBTValueDTO
from app.entities.models import BearerLinkHBT
from app.exception.request_processing_exception import RequestProcessingException


class HBTAdapter:

    @staticmethod
    def BearerLinkHbtToDTO(hbt: BearerLinkHBT) -> HBTDTO:
        ceil = HBTAdapter.ValueStrToHBTValueDTO(hbt.ceil)
        rate = HBTAdapter.ValueStrToHBTValueDTO(hbt.rate)
        return HBTDTO(ceil=ceil, rate=rate)

    @staticmethod
    def DTOToBearerLinkHbt(dto: HBTDTO) -> BearerLinkHBT:
        hbt = BearerLinkHBT()
        hbt.ceil = f"{dto.ceil.value}{dto.ceil.unit}"
        hbt.rate = f"{dto.rate.value}{dto.rate.unit}"
        return hbt

    @staticmethod
    def ValueStrToHBTValueDTO(input: str) -> HBTValueDTO:
        # Use regular expression to capture value and unit
        match = re.match(r"(\d+)(kbit|mbit|gbit)", input)

        if not match:
            raise RequestProcessingException(
                status_code=400, detail=f"Invalid format for rate string: {input}"
            )

        # Extract value and unit from the regex match
        value = int(match.group(1))
        unit = match.group(2)

        # Return an instance of HBTValueDTO
        return HBTValueDTO(value=value, unit=unit)
