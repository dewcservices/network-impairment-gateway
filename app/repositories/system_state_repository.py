from sqlalchemy.orm import Session

from app.entities.models import SystemState
from app.repositories.interfaces.isystem_state_repository import ISystemStateRepository


class SystemStateRepository(ISystemStateRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.id = 1
        self.not_set = 1

    def get(self) -> SystemState:
        system_state = (
            self.db_session.query(SystemState).filter(SystemState.id == self.id).first()
        )
        if not system_state:
            self.create()
            return (
                self.db_session.query(SystemState)
                .filter(SystemState.id == self.id)
                .first()
            )

        return system_state

    def set(self, bearer_id: int, uplink_env_id: int, downlink_env_id: int) -> bool:
        system_state = self.get()
        system_state.bearer_id = bearer_id
        system_state.uplink_environment_id = uplink_env_id
        system_state.downlink_environment_id = downlink_env_id
        self.db_session.commit()

    def create(self):
        system_state = SystemState(
            id=self.id,
            bearer_id=self.not_set,
            uplink_environment_id=self.not_set,
            downlink_environment_id=self.not_set,
        )
        self.db_session.add(system_state)
        self.db_session.commit()
