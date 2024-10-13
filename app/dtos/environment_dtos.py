from pydantic import BaseModel, Field

from app.dtos.hbt_dtos import HBT
from app.dtos.netem_dtos import NetemCorrupt, NetemDelay, NetemLoss


class EnvironmentNetem(BaseModel):
    delay: NetemDelay
    loss: NetemLoss
    corrupt: NetemCorrupt


class Environment(BaseModel):
    title: str = Field(
        ..., min_length=5, max_length=100, description="Title of the bearer"
    )
    description: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="A description of the satellite or bearer connection",
    )
    hbt: HBT = Field(..., description="The HBT model containing rate and ceil values")
    netem: EnvironmentNetem = Field(
        ..., description="The NETEM model containing delay, loss and corrupt values"
    )
