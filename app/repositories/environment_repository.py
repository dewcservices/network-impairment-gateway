from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from app.entities.models import Environment, EnvironmentNetem
from app.repositories.interfaces.ienvironment_repository import IEnvironmentRepository


class EnvironmentRepository(IEnvironmentRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all(self) -> List[Environment]:
        return self.db_session.query(Environment).all()

    def get_by_id(self, id: int) -> Optional[Environment]:
        return self.db_session.query(Environment).filter(Environment.id == id).first()

    # Get bearer by id, eager loading links, hbt, and netem relationships
    def get_by_id_eager(self, id: int) -> Optional[Environment]:
        return (
            self.db_session.query(Environment)
            .options(joinedload(Environment.environment_netem))
            .filter(Environment.id == id)
            .first()
        )

    # Update an existing bearer
    def update(
        self,
        id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Optional[Environment]:
        environment = self.get_by_id(id)
        if not environment:
            return None

        if title:
            environment.title = title
        if description:
            environment.description = description

        self.db_session.commit()
        return environment

    def create(
        self,
        title: str,
        description: str,
        netem_delay_time: int,
        netem_delay_jitter: int,
        netem_delay_correlation: int,
        netem_loss_percentage: float,
        netem_loss_interval: int,
        netem_loss_correlation: int,
        netem_corrupt_percentage: float,
        netem_corrupt_correlation: int,
    ) -> Environment:
        new_environment = Environment(title=title, description=description)
        new_netem = EnvironmentNetem(
            delay_time=netem_delay_time,
            delay_jitter=netem_delay_jitter,
            delay_correlation=netem_delay_correlation,
            loss_percentage=netem_loss_percentage,
            loss_interval=netem_loss_interval,
            loss_correlation=netem_loss_correlation,
            corrupt_percentage=netem_corrupt_percentage,
            corrupt_correlation=netem_corrupt_correlation,
        )

        self.db_session.add(new_environment)
        self.db_session.commit()
        new_netem.environment_id = new_environment.id
        self.db_session.add(new_netem)
        self.db_session.commit()
        return new_environment

    def delete(self, id: int):
        environment = self.get_by_id(id)
        if not environment:
            return None

        environment.active = False
        self.db_session.commit()
