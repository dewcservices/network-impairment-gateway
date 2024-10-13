# from sqlalchemy.orm import Session
# from app.database import SessionLocal
from app.services.bearer_service import BearerService
from app.services.environment_service import EnvironmentService
from app.services.interfaces.ibearer_service import IBearerService
from app.services.interfaces.ienvironment_service import IEnvironmentService
from app.services.interfaces.isetting_service import ISettingService
from app.services.setting_service import SettingService

ip_address = "172.18.0.1"
interface = "eth0"
uplink_qdisc_class = "1:1"
downlink_qdisc_class = "1:2"

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# def get_bearer_repository(db: Session = Depends(get_db)) -> IBearerRepository:
#     return BearerRepository(db)


# def get_env_repository(db: Session = Depends(get_db)) -> IEnvironmentRepository:
#     return EnvironmentRepository(db)


def get_bearer_service() -> IBearerService:
    return BearerService()


def get_env_service() -> IEnvironmentService:
    return EnvironmentService()


def get_setting_service() -> ISettingService:
    return SettingService()
