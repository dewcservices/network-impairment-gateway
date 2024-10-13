from typing import List

from app.dtos.bearer_dtos import Bearer
from app.dtos.response_dtos import Response
from app.services.interfaces.ibearer_service import IBearerService


class BearerService(IBearerService):

    async def get_all(self) -> List[Bearer]:
        return List[Bearer]()

    async def get(self, earer_id: int) -> Bearer:
        return Bearer()

    async def create(self, dto: Bearer) -> Response:
        return Response(msg="bearer create", isError=False)

    async def update(self, bearer_id: int, dto: Bearer) -> Response:
        return Response(msg="bearer update", isError=False)

    async def delete(self, bearer_id: int) -> Response:
        return Response(msg="bearer delete", isError=False)
