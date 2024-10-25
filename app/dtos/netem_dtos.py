from pydantic import BaseModel, Field


class NetemDelayDTO(BaseModel):
    time: int = Field(..., description="The delay time in milliseconds")
    jitter: int = Field(..., description="The jitter in milliseconds")
    correlation: int = Field(
        ..., ge=0, le=100, description="The correlation percentage between 0 and 100"
    )

    class ConfigDict:
        from_attributes = True  # Equivalent to orm_mode


class NetemLossDTO(BaseModel):
    percentage: float = Field(
        ..., ge=0.0, le=100.0, description="The loss percentage between 0 and 100"
    )
    interval: int = Field(..., description="The loss interval in milliseconds")
    correlation: int = Field(
        ..., ge=0, le=100, description="The correlation percentage between 0 and 100"
    )

    class ConfigDict:
        from_attributes = True  # Equivalent to orm_mode


class NetemCorruptDTO(BaseModel):
    percentage: float = Field(
        ..., ge=0.0, le=100.0, description="The corruption percentage between 0 and 100"
    )
    correlation: int = Field(
        ..., ge=0, le=100, description="The correlation percentage between 0 and 100"
    )

    class ConfigDict:
        from_attributes = True  # Equivalent to orm_mode
