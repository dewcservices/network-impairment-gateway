from app.services.interfaces.ibearer_service import IBearerService


class BearerService(IBearerService):

    async def get_all(self):
        return "list of bearers"

    async def get(self, bearer_id: int) -> str:
        return "bearer by id"

    async def create(self) -> str:
        return "bearer create"

    async def update(self, bearer_id: int) -> str:
        return "bearer update"

    async def delete(self, bearer_id: int) -> str:
        return "bearer delete"
