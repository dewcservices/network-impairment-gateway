from pydantic import BaseModel, Field

from app.dtos.netem_dtos import NetemCorruptDTO, NetemDelayDTO, NetemLossDTO


class EnvironmentNetemDTO(BaseModel):
    delay: NetemDelayDTO = Field(..., description="The Netem delay model")
    loss: NetemLossDTO = Field(..., description="The Netem delay model")
    corrupt: NetemCorruptDTO = Field(..., description="The Netem corrupt model")

    class ConfigDict:
        from_attributes = True  # Equivalent to orm_mode


class EnvironmentDTO(BaseModel):
    title: str = Field(
        ..., min_length=5, max_length=100, description="Title of the bearer"
    )
    description: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="A description of the satellite or bearer connection",
    )
    netem: EnvironmentNetemDTO = Field(
        ..., description="The NETEM model containing delay, loss and corrupt values"
    )

    class ConfigDict:
        from_attributes = True  # Equivalent to orm_mode


class EnvironmentDetailsDTO(BaseModel):
    id: int = Field(
        ...,
        description="Environment primary key",
    )
    title: str = Field(
        ..., min_length=5, max_length=100, description="Title of the bearer"
    )
    description: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="A description of the satellite or bearer connection",
    )

    class ConfigDict:
        from_attributes = True  # Equivalent to orm_mode
