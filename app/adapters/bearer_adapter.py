from typing import List

from app.dtos.bearer_dtos import (
    BearerDetailsDTO,
    BearerDTO,
    BearerLinkDTO,
    BearerNetemDTO,
)
from app.entities.models import Bearer, BearerLink, BearerLinkNetem


class BearerAdapter:

    @staticmethod
    def BearerToBearerDTO(bearer: Bearer) -> BearerDTO:
        return BearerDTO.model_validate(bearer)

    @staticmethod
    def BearerToBearerDetailsDTO(bearer: Bearer) -> BearerDetailsDTO:
        return BearerDetailsDTO.model_validate(bearer)

    @staticmethod
    def BearersToBearerDetailsDTOs(bearers: List[Bearer]) -> List[BearerDetailsDTO]:
        return [BearerAdapter.BearerToBearerDetailsDTO(bearer) for bearer in bearers]

    @staticmethod
    def BearerDTOToBearer(dto: BearerDTO) -> Bearer:
        # Convert Pydantic BearerDTO to SQLAlchemy Bearer using .dict() and **kwargs
        bearer_dict = dto.model_dump()

        # Convert img (HttpUrl type) to string if necessary
        if "img" in bearer_dict and bearer_dict["img"] is not None:
            bearer_dict["img"] = str(bearer_dict["img"])

        # Create and return SQLAlchemy Bearer model
        return Bearer(**bearer_dict)

    @staticmethod
    def BearerLinkToBearerLinkDTO(bearer_link: BearerLink) -> BearerLinkDTO:
        return BearerLinkDTO.model_validate(bearer_link)

    @staticmethod
    def BearerLinkDTOToBearerLink(dto: BearerLinkDTO) -> BearerLink:
        bearer_link_dict = dto.model_dump()
        return BearerLink(**bearer_link_dict)

    @staticmethod
    def BearerNetemToBearerNetemDTO(
        bearer_link_netem: BearerLinkNetem,
    ) -> BearerNetemDTO:
        return BearerLinkDTO.model_validate(bearer_link_netem)

    @staticmethod
    def BearerNetemDTOToBearerNetem(dto: BearerNetemDTO) -> BearerLinkNetem:
        bearer_link_netem_dict = dto.model_dump()
        return BearerLink(**bearer_link_netem_dict)
