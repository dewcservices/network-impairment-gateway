from typing import List

from app.dtos.environment_dtos import Environment
from app.dtos.response_dtos import Response
from app.services.interfaces.ienvironment_service import IEnvironmentService


class EnvironmentService(IEnvironmentService):

    async def get_all(self) -> List[Environment]:
        return List[Environment]

    async def get(self, env_id: int) -> Environment:
        return Environment()

    async def create(self, dto: Environment) -> Response:
        return Response(msg="environment create", isError=False)

    async def update(self, env_id: int, dto: Environment) -> Response:
        return Response(msg="environment update", isError=False)

    async def delete(self, env_id: int) -> Response:
        return Response(msg="environment delete", isError=False)
