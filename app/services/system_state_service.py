from app.adapters.system_state_adapter import SystemStateAdapter
from app.dtos.response_dtos import ResponseDTO
from app.dtos.system_dtos import SystemStateDTO
from app.repositories.interfaces.isystem_state_repository import ISystemStateRepository
from app.services.interfaces.isystem_state_service import ISystemStateService


class SystemStateService(ISystemStateService):

    def __init__(self, repo: ISystemStateRepository):
        self.repo = repo

    def get(self) -> SystemStateDTO:
        return SystemStateAdapter.SystemStateToDTO(self.repo.get())

    def set_impairment(self, payload: SystemStateDTO) -> ResponseDTO:
        self.repo.set(bearer_id=payload.bearer_id, env_id=payload.environment_id)
        return ResponseDTO(msg="Impairment set called", isError=False)

    def delete_htb_netem_qdiscs(self) -> ResponseDTO:
        return ResponseDTO(msg="htb and netem qdisc added", isError=False)
