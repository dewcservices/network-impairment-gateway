import os

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.repositories.bearer_repository import BearerRepository
from app.repositories.environment_repository import EnvironmentRepository
from app.repositories.interfaces.ibearer_repository import IBearerRepository
from app.repositories.interfaces.ienvironment_repository import IEnvironmentRepository
from app.repositories.interfaces.isystem_state_repository import ISystemStateRepository
from app.repositories.system_state_repository import SystemStateRepository
from app.seeding.seeding import seed_db
from app.services.bearer_service import BearerService
from app.services.debug_process_service import DebugProcessService
from app.services.environment_service import EnvironmentService
from app.services.interfaces.ibearer_service import IBearerService
from app.services.interfaces.ienvironment_service import IEnvironmentService
from app.services.interfaces.iprocess_service import IProcessService
from app.services.interfaces.isystem_state_service import ISystemStateService
from app.services.subprocess_service import SubprocessService
from app.services.system_state_service import SystemStateService

# Load values from environment variables with defaults
uplink_interface = os.getenv("UPLINK_INTERFACE", "eth0")
downlink_interface = os.getenv("DOWNLINK_INTERFACE", "eth1")
mock_process_calls = os.getenv("MOCK_PROCESS_CALLS", "True").lower() == "true"
seeded = os.getenv("DATABASE_SEEDED", "FALSE").lower() == "true"


def get_db():
    global seeded
    db = SessionLocal()
    if not seeded:
        seed_db(db=db)
        seeded = True
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


def get_process_service() -> IProcessService:
    global mock_process_calls
    if mock_process_calls:
        return DebugProcessService()
    else:
        return SubprocessService()


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
    bearer_repo: IBearerRepository = Depends(get_bearer_repository),
    env_repo: IEnvironmentRepository = Depends(get_env_repository),
    process_svc: IEnvironmentRepository = Depends(get_process_service),
) -> ISystemStateService:

    global downlink_interface
    global uplink_interface

    return SystemStateService(
        repo=repo,
        bearer_repo=bearer_repo,
        env_repo=env_repo,
        process_svc=process_svc,
        uplink_interface=uplink_interface,
        downlink_interface=downlink_interface,
    )
