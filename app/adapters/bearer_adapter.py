from typing import List

from app.adapters.dto_to_model_util import DtoToModelUtil
from app.adapters.hbt_adapter import HBTAdapter
from app.adapters.netem_adapter import NetemAdapter
from app.dtos.bearer_dtos import (
    BearerDetailsDTO,
    BearerDTO,
    BearerLinkDTO,
    BearerNetemDTO,
)
from app.dtos.hbt_dtos import HBTDTO
from app.entities.models import Bearer, BearerLink, BearerLinkHBT, BearerLinkNetem


class BearerAdapter:

    @staticmethod
    def BearerToBearerDetailsDTO(bearer: Bearer) -> BearerDetailsDTO:
        return BearerDetailsDTO.model_validate(
            DtoToModelUtil.map_object_to_dto(bearer, BearerDetailsDTO)
        )

    @staticmethod
    def BearersToBearerDetailsDTOs(bearers: List[Bearer]) -> List[BearerDetailsDTO]:
        return [BearerAdapter.BearerToBearerDetailsDTO(bearer) for bearer in bearers]

    @staticmethod
    def BearerToBearerDTO(bearer: Bearer) -> BearerDTO:
        dict_dto = DtoToModelUtil.map_object_to_dto(bearer, BearerDTO, {"links": {}})
        return BearerDTO.model_validate(dict_dto)

    @staticmethod
    def BearerDTOToBearer(dto: BearerDTO) -> Bearer:
        # Convert Pydantic BearerDTO to SQLAlchemy Bearer using .dict() and **kwargs
        bearer_dict = dto.model_dump()

        # Convert img (HttpUrl type) to string if necessary
        if "img" in bearer_dict and bearer_dict["img"] is not None:
            bearer_dict["img"] = str(bearer_dict["img"])

        # Filter out keys that are not valid attributes of the SQLAlchemy model
        # used to remove bearer_dict.links
        valid_keys = {k: v for k, v in bearer_dict.items() if hasattr(Bearer, k)}

        # Create and return SQLAlchemy Bearer model
        return Bearer(**valid_keys)

    @staticmethod
    def BearerLinkToBearerLinkDTO(bearer_link: BearerLink) -> BearerLinkDTO:
        dto = BearerLinkDTO()
        dto.netem = BearerAdapter.BearerNetemToBearerNetemDTO(
            bearer_link.bearer_link_netem
        )
        dto.hbt = BearerAdapter.BearerNetemToBearerHtbDTO(bearer_link.bearer_link_hbt)

        # nest to a full bearer link with all children
        return dto

    @staticmethod
    def BearerNetemToBearerNetemDTO(
        bearer_link_netem: BearerLinkNetem,
    ) -> BearerNetemDTO:
        dto = BearerNetemDTO()
        dto.delay = NetemAdapter.DelayDTO(
            time=bearer_link_netem.delay_time,
            jitter=bearer_link_netem.delay_jitter,
            correlation=bearer_link_netem.delay_correlation,
        )
        dto.loss = NetemAdapter.LossDTO(
            percentage=bearer_link_netem.loss_percentage,
            interval=bearer_link_netem.loss_interval,
            correlation=bearer_link_netem.loss_correlation,
        )
        return BearerNetemDTO

    @staticmethod
    def BearerNetemToBearerHtbDTO(bearer_link_hbt: BearerLinkHBT) -> HBTDTO:
        return HBTAdapter.BearerLinkHbtToDTO(bearer_link_hbt)
