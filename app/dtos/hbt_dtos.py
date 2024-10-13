from typing import Literal

from pydantic import BaseModel, Field


class HBTValue(BaseModel):
    value: int = Field(..., description="The rate/ceil value as an integer")
    unit: Literal["kbit", "mbit", "gbit"] = Field(
        ..., description="The unit for the value, can be 'kbit', 'mbit', or 'gbit'"
    )


class HBT(BaseModel):
    rate: HBTValue
    ceil: HBTValue
