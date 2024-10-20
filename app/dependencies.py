from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.entities.models import BearerLinkType
from app.repositories.bearer_repository import BearerRepository
from app.repositories.environment_repository import EnvironmentRepository
from app.repositories.interfaces.ibearer_repository import IBearerRepository
from app.repositories.interfaces.ienvironment_repository import IEnvironmentRepository
from app.repositories.interfaces.isystem_state_repository import ISystemStateRepository
from app.repositories.system_state_repository import SystemStateRepository
from app.services.bearer_service import BearerService
from app.services.environment_service import EnvironmentService
from app.services.interfaces.ibearer_service import IBearerService
from app.services.interfaces.ienvironment_service import IEnvironmentService
from app.services.interfaces.isystem_state_service import ISystemStateService
from app.services.system_state_service import SystemStateService

ip_address = "172.18.0.1"
interface = "eth0"
uplink_qdisc_class = "1:1"
downlink_qdisc_class = "1:2"

seeded = False


def seed_db(db: Session):
    uplink = BearerLinkType(title="Uplink")
    downlink = BearerLinkType(title="Downlink")
    db.add(uplink)
    db.add(downlink)
    db.commit()


def get_db():
    db = SessionLocal()
    if not seeded:
        seed_db(db=db)
    try:
        yield db
    finally:
        db.close()


def get_bearer_repository(db_session: Session = Depends(get_db)) -> IBearerRepository:
    return BearerRepository(db_session)


def get_env_repository(db_session: Session = Depends(get_db)) -> IEnvironmentRepository:
    return EnvironmentRepository(db_session)


def get_system_state_repository(
    db_session: Session = Depends(get_db),
) -> ISystemStateRepository:
    return SystemStateRepository(db_session)


def get_bearer_service(
    repo: IBearerRepository = Depends(get_bearer_repository),
) -> IBearerService:
    return BearerService(repo)


def get_env_service(
    repo: IEnvironmentRepository = Depends(get_env_repository),
) -> IEnvironmentService:
    return EnvironmentService(repo)


def get_setting_service(
    repo: ISystemStateRepository = Depends(get_system_state_repository),
) -> ISystemStateService:
    return SystemStateService(repo)
