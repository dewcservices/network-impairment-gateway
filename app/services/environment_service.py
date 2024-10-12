from app.services.interfaces.ienvironment_service import IEnvironmentService


class EnvironmentService(IEnvironmentService):

    async def get_all(self):
        return "list of environments"

    async def get(self, env_id: int) -> str:
        return "environment by id"

    async def create(self) -> str:
        return "environment create"

    async def update(self, env_id: int) -> str:
        return "environment update"

    async def delete(self, env_id: int) -> str:
        return "environment delete"
