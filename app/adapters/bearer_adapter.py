from typing import List

from app.adapters.dto_to_model_util import DtoToModelUtil
from app.adapters.hbt_adapter import HBTAdapter
from app.adapters.netem_adapter import NetemAdapter
from app.constants import LinkTypes
from app.dtos.bearer_dtos import (
    BearerDetailsDTO,
    BearerDTO,
    BearerLinkDTO,
    BearerNetemDTO,
)
from app.dtos.hbt_dtos import HBTDTO
from app.entities.models import Bearer, BearerLink, BearerLinkHBT, BearerLinkNetem
from app.exception.request_processing_exception import RequestProcessingException


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
    def BearerToBearerDTO(bearer: Bearer) -> BearerDTO:
        if bearer is None:
            raise RequestProcessingException(
                status_code=400, detail="Bearer was empty while adapting to dto"
            )
        dict_dto = DtoToModelUtil.map_object_to_dto(bearer, BearerDTO, {"links": {}})
        dto = BearerDTO.model_validate(dict_dto)

        for link in bearer.bearer_links:
            if isinstance(link, BearerLink):
                print(
                    f"link_type_id: {link.link_type_id}, type: {type(link.link_type_id)}"
                )
                if link.link_type_id == int(LinkTypes.UPLINK.value):
                    dto.links[LinkTypes.UPLINK.name] = (
                        BearerAdapter.BearerLinkToBearerLinkDTO(link)
                    )
                elif link.link_type_id == int(LinkTypes.DOWNLINK.value):
                    dto.links[LinkTypes.DOWNLINK.name] = (
                        BearerAdapter.BearerLinkToBearerLinkDTO(link)
                    )
        return dto

    @staticmethod
    def BearerLinkToBearerLinkDTO(bearer_link: BearerLink) -> BearerLinkDTO:
        if bearer_link is None:
            raise RequestProcessingException(
                status_code=400, detail="Bearer link was empty while adapting to dto"
            )
        netem = BearerAdapter.BearerNetemToBearerNetemDTO(bearer_link.bearer_link_netem)
        hbt = BearerAdapter.BearerNetemToBearerHtbDTO(bearer_link.bearer_link_hbt)
        # nest to a full bearer link with all children
        return BearerLinkDTO(netem=netem, hbt=hbt)

    @staticmethod
    def BearerNetemToBearerNetemDTO(
        bearer_link_netem: BearerLinkNetem,
    ) -> BearerNetemDTO:
        if bearer_link_netem is None:
            raise RequestProcessingException(
                status_code=400,
                detail="Bearer link network emulation settings was empty while adapting to dto",
            )
        delay = NetemAdapter.DelayDTO(
            time=bearer_link_netem.delay_time,
            jitter=bearer_link_netem.delay_jitter,
            correlation=bearer_link_netem.delay_correlation,
        )
        loss = NetemAdapter.LossDTO(
            percentage=bearer_link_netem.loss_percentage,
            interval=bearer_link_netem.loss_interval,
            correlation=bearer_link_netem.loss_correlation,
        )
        return BearerNetemDTO(delay=delay, loss=loss)

    @staticmethod
    def BearerNetemToBearerHtbDTO(bearer_link_hbt: BearerLinkHBT) -> HBTDTO:
        if bearer_link_hbt is None:
            raise RequestProcessingException(
                status_code=400,
                detail="Bearer link hbt settings was empty while adapting to dto",
            )
        return HBTAdapter.BearerLinkHbtToDTO(bearer_link_hbt)
