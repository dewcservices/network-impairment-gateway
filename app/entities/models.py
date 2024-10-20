from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from app.database import Base, engine


class SystemState(Base):
    __tablename__ = "system_states"
    id = Column(Integer, primary_key=True, autoincrement=True)
    bearer_id = Column(Integer)
    environment_id = Column(Integer)
    # Timestamp column for when the row is updated
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    def __repr__(self):
        return f"<SystemState(bearer_id='{self.bearer_id}', environment_id='{self.environment_id}')>"


class Bearer(Base):
    __tablename__ = "bearers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    img = Column(String(255), nullable=True)  # Assuming this is a URL string
    active = Column(Boolean, nullable=True, default=True)

    # Relationship with BearerLink
    bearer_links = relationship(
        "BearerLink", back_populates="bearer", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Bearer(title='{self.title}', description='{self.description}', img='{self.img}')>"


class BearerLinkType(Base):
    __tablename__ = "bearer_link_types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, unique=True)

    # Relationship with BearerLink
    bearer_links = relationship("BearerLink", back_populates="bearer_link_type")

    def __repr__(self):
        return f"<BearerLinkType(title='{self.title}')>"


# BearerLink model representing uplink and downlink links
class BearerLink(Base):
    __tablename__ = "bearer_links"

    id = Column(Integer, primary_key=True, autoincrement=True)
    bearer_id = Column(Integer, ForeignKey("bearers.id"), nullable=False)
    link_type_id = Column(
        Integer, ForeignKey("bearer_link_types.id"), nullable=False
    )  # 'uplink' or 'downlink'

    # Relationship back to Bearer
    bearer = relationship("Bearer", back_populates="bearer_links")

    # Relationship back to BearerLinkType
    bearer_link_type = relationship("BearerLinkType", back_populates="bearer_links")

    # Relationship with HBT, Netem (These will store the detailed network characteristics)
    bearer_link_hbt = relationship(
        "BearerLinkHBT",
        uselist=False,
        back_populates="bearer_link",
        cascade="all, delete-orphan",
    )
    bearer_link_netem = relationship(
        "BearerLinkNetem",
        uselist=False,
        back_populates="bearer_link",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<BearerLinkbearer_id='{self.bearer_id}', link_type_id='{self.link_type_id}')>"


# HBT (Hierarchical Token Bucket) for the rate and ceil values
class BearerLinkHBT(Base):
    __tablename__ = "bearer_link_hbts"

    bearer_link_id = Column(
        Integer, ForeignKey("bearer_links.id"), primary_key=True, nullable=False
    )

    rate = Column(String(10), nullable=False)  # 'kbit', 'mbit', 'gbit'
    ceil = Column(String(10), nullable=False)  # 'kbit', 'mbit', 'gbit'

    bearer_link = relationship("BearerLink", back_populates="bearer_link_hbt")

    def __repr__(self):
        return f"<HBT(rate='{self.rate}', ceil='{self.ceil}')>"


# Netem (Network Emulation) for delay, jitter, loss, etc.
class BearerLinkNetem(Base):
    __tablename__ = "bearer_link_netems"

    bearer_link_id = Column(
        Integer, ForeignKey("bearer_links.id"), primary_key=True, nullable=False
    )

    # Delay settings
    delay_time = Column(Integer, nullable=False, default=0)  # 'ms'

    # Jitter settings
    delay_jitter = Column(Integer, nullable=False, default=0)  # 'ms'
    delay_correlation = Column(
        Integer, nullable=False, default=0
    )  # percentage value (0-100)

    # Loss settings
    loss_percentage = Column(Integer, nullable=False, default=0)  # percentage
    loss_interval = Column(Integer, nullable=False, default=0)  # 'ms'
    loss_correlation = Column(
        Integer, nullable=False, default=0
    )  # percentage value (0-100)

    bearer_link = relationship("BearerLink", back_populates="bearer_link_netem")

    def __repr__(self):
        return f"<BearerNetem(delay='{self.delay_time}', jitter='{self.delay_jitter}', correlation='{self.delay_correlation}%', loss_percentage='{self.loss_percentage}', loss_interval='{self.loss_interval}', loss_correlation='{self.loss_correlation}')>"


class Environment(Base):
    __tablename__ = "environments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    active = Column(Boolean, nullable=True, default=True)

    # Relationship with BearerLink
    environment_netem = relationship(
        "EnvironmentNetem", back_populates="environment", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Environment(title='{self.title}', description='{self.description}')>"


class EnvironmentNetem(Base):
    __tablename__ = "environment_netems"
    environment_id = Column(
        Integer, ForeignKey("environments.id"), primary_key=True, nullable=False
    )

    # Delay settings
    delay_time = Column(Integer, nullable=False, default=0)  # 'ms'

    # Jitter settings
    delay_jitter = Column(Integer, nullable=False, default=0)  # 'ms'
    delay_correlation = Column(
        Integer, nullable=False, default=0
    )  # percentage value (0-100)

    # Loss settings
    loss_percentage = Column(Integer, nullable=False, default=0)  # percentage
    loss_interval = Column(Integer, nullable=False, default=0)  # 'ms'
    loss_correlation = Column(
        Integer, nullable=False, default=0
    )  # percentage value (0-100)

    corrupt_percentage = Column(Integer, nullable=False, default=0)  # percentage
    corrupt_correlation = Column(
        Integer, nullable=False, default=0
    )  # percentage value (0-100)

    environment = relationship("Environment", back_populates="environment_netem")

    def __repr__(self):
        return f"<BearerNetem(delay_time='{self.delay_time}', delay_jitter='{self.delay_jitter}', delay_correlation='{self.delay_correlation}%', loss_percentage='{self.loss_percentage}', loss_interval='{self.loss_interval}', loss_correlation='{self.loss_correlation}', corrupt_percentage='{self.corrupt_percentage}', corrupt_correlation='{self.corrupt_correlation}')>"


Base.metadata.create_all(bind=engine)
