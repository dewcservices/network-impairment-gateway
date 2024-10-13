from typing import Optional

from pydantic import BaseModel, Field, HttpUrl

from app.dtos.hbt_dtos import HBT
from app.dtos.netem_dtos import NetemDelay, NetemLoss


class BearerNetem(BaseModel):
    delay: NetemDelay
    loss: NetemLoss


class BearerLink(BaseModel):
    hbt: HBT = Field(..., description="The HBT model containing rate and ceil values")
    netem: BearerNetem = Field(
        ..., description="The NETEM model containing delay, loss values"
    )


class Bearer(BaseModel):
    title: str = Field(
        ..., min_length=5, max_length=100, description="Title of the bearer"
    )
    description: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="A description of the satellite or bearer connection",
    )
    img: Optional[HttpUrl] = Field(
        None, description="A URL for an image representing the bearer"
    )
    links: BearerLink
    downlink: BearerLink
