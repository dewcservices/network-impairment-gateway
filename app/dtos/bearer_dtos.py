from typing import Dict, Optional

from pydantic import BaseModel, Field

from app.dtos.hbt_dtos import HBTDTO
from app.dtos.netem_dtos import NetemDelayDTO, NetemLossDTO


class BearerNetemDTO(BaseModel):
    delay: NetemDelayDTO = Field(..., description="The Netem delay model")
    loss: NetemLossDTO = Field(..., description="The Netem loss model")

    class ConfigDict:
        from_attributes = True  # Equivalent to orm_mode


class BearerLinkDTO(BaseModel):
    hbt: HBTDTO = Field(
        ..., description="The HBT model containing rate and ceil values"
    )
    netem: BearerNetemDTO = Field(
        ..., description="The NETEM model containing delay, loss values"
    )

    class ConfigDict:
        from_attributes = True  # Equivalent to orm_mode


class BearerDTO(BaseModel):
    title: str = Field(
        ..., min_length=2, max_length=100, description="Title of the bearer"
    )
    description: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="A description of the satellite or bearer connection",
    )
    img: Optional[str] = Field(
        None, description="A URL for an image representing the bearer"
    )
    links: Dict[str, BearerLinkDTO] = Field(..., description="Bearer Links")

    class ConfigDict:
        from_attributes = True  # Equivalent to orm_mode


class BearerDetailsDTO(BaseModel):
    id: int = Field(
        ...,
        description="Environment primary key",
    )
    title: str = Field(
        ..., min_length=2, max_length=100, description="Title of the bearer"
    )
    description: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="A description of the satellite or bearer connection",
    )
    img: Optional[str] = Field(
        None, description="A URL for an image representing the bearer"
    )

    class ConfigDict:
        from_attributes = True  # Equivalent to orm_mode
