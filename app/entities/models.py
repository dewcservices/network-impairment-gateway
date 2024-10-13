from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class SystemState(Base):
    bearer_id = Column(Integer, primary_key=True, autoincrement=True)
    environment_id = Column(Integer, primary_key=True, autoincrement=True)
    # Timestamp column for when the row is updated
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    def __repr__(self):
        return f"<SystemState(bearer_id='{self.bearer_id}', environment_id='{self.environment_id}')>"


class Bearer(Base):
    __tablename__ = "bearer"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    img = Column(String(255), nullable=True)  # Assuming this is a URL string

    # Relationship with BearerLink
    bearer_links = relationship(
        "BearerLink", back_populates="bearer", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Bearer(title='{self.title}', description='{self.description}', img='{self.img}')>"


class BearerLinkType(Base):
    __tablename__ = "bearer_link_type"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)

    # Relationship with BearerLink
    bearer_links = relationship(
        "BearerLink", back_populates="bearer_link_type", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<BearerLinkType(title='{self.title}')>"


# BearerLink model representing uplink and downlink links
class BearerLink(Base):
    __tablename__ = "bearer_link"

    id = Column(Integer, primary_key=True, autoincrement=True)
    bearer_id = Column(Integer, ForeignKey("bearer.id"), nullable=False)
    link_type_id = Column(
        Integer, ForeignKey("bearer_link_type.id"), nullable=False
    )  # 'uplink' or 'downlink'

    # Relationship back to BearerLinkType
    bearer_link_type = relationship("BearerLinkType", back_populates="bearer_links")
    # Relationship back to Bearer
    bearer = relationship("Bearer", back_populates="bearer_links")

    # Relationship with HBT, Netem (These will store the detailed network characteristics)
    hbt = relationship(
        "BearerHBT",
        uselist=False,
        back_populates="bearer_link",
        cascade="all, delete-orphan",
    )
    netem = relationship(
        "BearerNetem",
        uselist=False,
        back_populates="bearer_link",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<BearerLink(link_type='{self.link_type}')>"


# HBT (Hierarchical Token Bucket) for the rate and ceil values
class BearerHBT(Base):
    __tablename__ = "bearer_hbt"

    id = Column(Integer, primary_key=True, autoincrement=True)
    bearer_link_id = Column(Integer, ForeignKey("bearer_link.id"), nullable=False)

    rate = Column(String(10), nullable=False)  # 'kbit', 'mbit', 'gbit'
    ceil = Column(String(10), nullable=False)  # 'kbit', 'mbit', 'gbit'

    bearer_link = relationship("BearerLink", back_populates="bearer_hbt")

    def __repr__(self):
        return f"<HBT(rate='{self.rate}', ceil='{self.ceil}')>"


# Netem (Network Emulation) for delay, jitter, loss, etc.
class BearerNetem(Base):
    __tablename__ = "bearer_netem"

    id = Column(Integer, primary_key=True, autoincrement=True)
    bearer_link_id = Column(Integer, ForeignKey("bearer_link.id"), nullable=False)

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

    bearer_link = relationship("BearerLink", back_populates="bearer_netem")

    # Enforce that loss_percentage is between 0 and 100
    __table_args__ = (
        CheckConstraint(
            "loss_percentage >= 0 AND loss_percentage <= 100",
            name="check_loss_percentage",
        ),
        CheckConstraint(
            "delay_correlation >= 0 AND delay_correlation <= 100",
            name="check_delay_correlation",
        ),
    )

    def __repr__(self):
        return f"<BearerNetem(delay='{self.delay_time}', jitter='{self.delay_jitter}', correlation='{self.delay_correlation}%', loss_percentage='{self.loss_percentage}', loss_interval='{self.loss_interval}', loss_correlation='{self.loss_correlation}')>"


class Environment(Base):
    __tablename__ = "environment"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)

    # Relationship with BearerLink
    environment_netem = relationship(
        "EnvironmentNetem", back_populates="environment", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Environment(title='{self.title}', description='{self.description}')>"


class EnvironmentNetem(Base):
    __tablename__ = "environment_netem"
    id = Column(Integer, primary_key=True, autoincrement=True)
    environment_id = Column(Integer, ForeignKey("environment.id"), nullable=False)

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
