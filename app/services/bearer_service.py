from typing import List

from app.dtos.bearer_dtos import BearerDTO
from app.dtos.response_dtos import ResponseDTO
from app.repositories.interfaces.ibearer_repository import IBearerRepository
from app.services.interfaces.ibearer_service import IBearerService


class BearerService(IBearerService):

    def __init__(self, repo: IBearerRepository):
        self.repo = repo

    def get_all(self) -> List[BearerDTO]:
        return self.repo.get_all()

    def get(self, bearer_id: int) -> BearerDTO:
        return self.repo.get_by_id_eager(bearer_id)

    def create(self, dto: BearerDTO) -> ResponseDTO:
        self.repo.create(title=dto.title, description=dto.description, img=str(dto.img))
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
        # self.repo.update(id=bearer_id, title=dto.title, description=dto.description, img=dto.img)
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
        self.repo.delete(bearer_id)
        return ResponseDTO(msg="bearer deleted", isError=False)
