from typing import List

from fastapi import HTTPException

from app.adapters.bearer_adapter import BearerAdapter
from app.adapters.hbt_adapter import HBTAdapter
from app.constants import LinkTypes
from app.dtos.bearer_dtos import BearerDetailsDTO, BearerDTO, BearerLinkDTO
from app.dtos.response_dtos import ResponseDTO
from app.repositories.interfaces.ibearer_repository import IBearerRepository
from app.services.interfaces.ibearer_service import IBearerService


class BearerService(IBearerService):

    def __init__(self, repo: IBearerRepository):
        self.repo = repo

    def get_all(self) -> List[BearerDetailsDTO]:
        return BearerAdapter.BearersToBearerDetailsDTOs(self.repo.get_all())

    def get(self, bearer_id: int) -> BearerDTO:
        bearer = self.repo.get_by_id_eager(bearer_id)
        if bearer is None:
            raise HTTPException(
                status_code=404, detail=f"Bearer id {bearer_id} not found"
            )
        return BearerAdapter.BearerToBearerDTO(bearer)

    def create(self, dto: BearerDTO) -> ResponseDTO:
        bearer = self.repo.create(
            title=dto.title, description=dto.description, img=str(dto.img)
        )

        if not bearer:
            raise HTTPException(
                status_code=404, detail=f"Failed to create Bearer {dto.title}"
            )

        self.create_link(
            bearer_id=bearer.id,
            link_type_id=LinkTypes.UPLINK.value,
            dto=dto.links[LinkTypes.UPLINK.name],
        )
        self.create_link(
            bearer_id=bearer.id,
            link_type_id=LinkTypes.DOWNLINK.value,
            dto=dto.links[LinkTypes.DOWNLINK.name],
        )
        return ResponseDTO(msg="bearer created", isError=False)

    def create_link(
        self, bearer_id: int, link_type_id: int, link: BearerLinkDTO
    ) -> bool:
        hbt = HBTAdapter.DTOToBearerLinkHbt(dto=link.hbt)
        netem = link.netem
        self.repo.create_bearer_link(
            id=bearer_id,
            link_type_id=link_type_id,
            hbt_ceil=hbt.ceil,
            hbt_rate=hbt.rate,
            netem_delay_time=netem.delay.time,
            netem_delay_jitter=netem.delay.jitter,
            netem_loss_correlation=netem.delay.correlation,
            netem_loss_interval=netem.loss.interval,
            netem_loss_percentage=netem.loss.percentage,
        )
        return True

    def update(self, bearer_id: int, dto: BearerDTO) -> ResponseDTO:
        bearer = self.repo.update(
            id=bearer_id, title=dto.title, description=dto.description, img=dto.img
        )
        if not bearer:
            raise HTTPException(
                status_code=404, detail=f"Bearer id {bearer_id} not found"
            )
        # TODO: implement Bearer Netem and HBT Update approach in repo and this service
        # for link in dto.links:
        #     self.repo.create_bearer_link(
        #         id=bearer.id,
        #         link_type_id=link.link_type_id,
        #         hbt_rate=link.hbt_rate,
        #         hbt_ceil=link.hbt_ceil,
        #     )
        # return bearer.id
        return ResponseDTO(msg="bearer updated", isError=False)

    def delete(self, bearer_id: int) -> ResponseDTO:
        result = self.repo.delete(bearer_id)

        if not result:
            raise HTTPException(
                status_code=404, detail=f"Bearer id {bearer_id} not found"
            )

        return ResponseDTO(msg="bearer deleted", isError=False)
