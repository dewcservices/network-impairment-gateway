from sqlalchemy.orm import Session

from app.entities.models import BearerLinkType
from app.repositories.bearer_repository import BearerRepository
from app.repositories.environment_repository import EnvironmentRepository
from app.repositories.interfaces.ibearer_repository import IBearerRepository
from app.repositories.interfaces.ienvironment_repository import IEnvironmentRepository
from app.seeding.bearers import (
    seed_4g_bearer,
    seed_5g_bearer,
    seed_commercial_maritime_bearer,
    seed_fixed_internet_bearer,
    seed_optus_c1_bearer,
)
from app.seeding.environments import (
    seed_clean_env,
    seed_congested_4g_env,
    seed_disconnected_env,
    seed_disrupted_env,
    seed_intermittent_env,
    seed_limited_env,
)


def seed_bearers(bearer_repo: IBearerRepository):
    seed_optus_c1_bearer(bearer_repo)
    seed_commercial_maritime_bearer(bearer_repo)
    seed_4g_bearer(bearer_repo)
    seed_5g_bearer(bearer_repo)
    seed_fixed_internet_bearer(bearer_repo)


def seed_environments(env_repo: IEnvironmentRepository):
    seed_clean_env(env_repo)
    seed_disconnected_env(env_repo)
    seed_disrupted_env(env_repo)
    seed_intermittent_env(env_repo)
    seed_limited_env(env_repo)
    seed_congested_4g_env(env_repo)


def seed_bearer_link_types(db: Session):
    uplink = BearerLinkType(title="Uplink")
    downlink = BearerLinkType(title="Downlink")
    db.add(uplink)
    db.add(downlink)
    db.commit()


def seed_db(db: Session):
    bearer_repo = BearerRepository(db)
    env_repo = EnvironmentRepository(db)
    seed_bearer_link_types(db)
    seed_bearers(bearer_repo)
    seed_environments(env_repo)
