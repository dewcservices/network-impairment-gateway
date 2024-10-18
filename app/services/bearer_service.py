from typing import List

from fastapi import HTTPException

from app.adapters.bearer_adapter import BearerAdapter
from app.dtos.bearer_dtos import BearerDetailsDTO, BearerDTO
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
        # TODO: need to iterate through the dictionary of links
        # TODO: should we just have the dto require up and downlink settings?
        # for link in dto.links:
        #     self.repo.create_bearer_link(
        #         id=bearer.id,
        #         link_type_id=link.link_type_id,
        #         hbt_rate=link.hbt_rate,
        #         hbt_ceil=link.hbt_ceil,
        #     )
        # return bearer.id
        return ResponseDTO(msg="bearer created", isError=False)

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
