from typing import Literal

from pydantic import BaseModel, Field


class HBTValueDTO(BaseModel):
    value: int = Field(..., description="The rate/ceil value as an integer")
    unit: Literal["kbit", "mbit", "gbit"] = Field(
        ..., description="The unit for the value, can be 'kbit', 'mbit', or 'gbit'"
    )


class HBTDTO(BaseModel):
    rate: HBTValueDTO = Field(..., description="The rate value")
    ceil: HBTValueDTO = Field(..., description="The ceil value")
