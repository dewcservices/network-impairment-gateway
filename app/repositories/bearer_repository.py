from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from app.entities.models import Bearer, BearerLink, BearerLinkHBT, BearerLinkNetem
from app.repositories.interfaces.ibearer_repository import IBearerRepository


class BearerRepository(IBearerRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    # Get all bearers
    def get_all(self) -> List[Bearer]:
        return self.db_session.query(Bearer).all()

    # Get bearer by id, eager loading links, hbt, and netem relationships
    def get_by_id(self, id: int) -> Optional[Bearer]:
        return self.db_session.query(Bearer).filter(Bearer.id == id).first()

    # Get bearer by id, eager loading links, hbt, and netem relationships
    def get_by_id_eager(self, id: int) -> Optional[Bearer]:
        return (
            self.db_session.query(Bearer)
            .options(
                joinedload(Bearer.bearer_links).joinedload(BearerLink.bearer_link_hbt),
                joinedload(Bearer.bearer_links).joinedload(
                    BearerLink.bearer_link_netem
                ),
            )
            .filter(Bearer.id == id)
            .first()
        )

    # Update an existing bearer
    def update(
        self,
        id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        img: Optional[str] = None,
    ) -> Optional[Bearer]:
        bearer = self.get_by_id(id)
        if not bearer:
            return None

        if title:
            bearer.title = title
        if description:
            bearer.description = description
        if img:
            bearer.img = img

        self.db_session.commit()
        return bearer

    def create(self, title: str, description: str, img: Optional[str] = None) -> Bearer:
        new_bearer = Bearer(title=title, description=description, img=img)
        self.db_session.add(new_bearer)
        self.db_session.commit()
        return new_bearer

        # Create a bearer link with HBT and Netem configuration

    def create_bearer_link(
        self,
        id: int,
        link_type_id: int,
        hbt_rate: str,
        hbt_ceil: str,
        netem_delay_time: int,
        netem_delay_jitter: int,
        netem_loss_percentage: float,
        netem_loss_interval: int,
        netem_loss_correlation: int,
    ) -> BearerLink:
        new_link = BearerLink(bearer_id=id, link_type_id=link_type_id)

        new_hbt = BearerLinkHBT(rate=hbt_rate, ceil=hbt_ceil)
        new_netem = BearerLinkNetem(
            delay_time=netem_delay_time,
            delay_jitter=netem_delay_jitter,
            loss_percentage=netem_loss_percentage,
            loss_interval=netem_loss_interval,
            loss_correlation=netem_loss_correlation,
        )

        new_link.hbt = new_hbt
        new_link.netem = new_netem

        self.db_session.add(new_link)
        self.db_session.commit()
        new_hbt.bearer_link_id = new_link.id
        new_netem.bearer_link_id = new_link.id

        self.db_session.add(new_hbt)
        self.db_session.add(new_netem)
        self.db_session.commit()

        return new_link

    # Update bearer link, HBT, and Netem configuration
    def update_bearer_link(
        self,
        link_id: int,
        hbt_rate: Optional[str] = None,
        hbt_ceil: Optional[str] = None,
        netem_delay_time: Optional[int] = None,
        netem_delay_jitter: Optional[int] = None,
        netem_loss_percentage: Optional[float] = None,
        netem_loss_interval: Optional[int] = None,
        netem_loss_correlation: Optional[int] = None,
    ) -> Optional[BearerLink]:
        link = (
            self.db_session.query(BearerLink).filter(BearerLink.id == link_id).first()
        )
        if not link:
            return None

        # Update HBT
        if hbt_rate:
            link.hbt.rate = hbt_rate
        if hbt_ceil:
            link.hbt.ceil = hbt_ceil

        # Update Netem
        if netem_delay_time is not None:
            link.netem.delay_time = netem_delay_time
        if netem_delay_jitter is not None:
            link.netem.delay_jitter = netem_delay_jitter
        if netem_loss_percentage is not None:
            link.netem.loss_percentage = netem_loss_percentage
        if netem_loss_interval is not None:
            link.netem.loss_interval = netem_loss_interval
        if netem_loss_correlation is not None:
            link.netem.loss_correlation = netem_loss_correlation

        self.db_session.commit()
        return link

    def delete(self, id: int) -> bool:
        bearer = self.get_by_id(id)
        if not bearer:
            return False

        bearer.active = False
        self.db_session.commit()
        return True
