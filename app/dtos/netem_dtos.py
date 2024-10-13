from pydantic import BaseModel, Field


class NetemDelay(BaseModel):
    time: int = Field(..., description="The delay time in milliseconds")
    jitter: int = Field(..., description="The jitter in milliseconds")
    correlation: int = Field(
        ..., ge=0, le=100, description="The correlation percentage between 0 and 100"
    )


class NetemLoss(BaseModel):
    percentage: int = Field(
        ..., ge=0, le=100, description="The loss percentage between 0 and 100"
    )
    interval: int = Field(..., description="The loss interval in milliseconds")
    correlation: int = Field(
        ..., ge=0, le=100, description="The correlation percentage between 0 and 100"
    )


class NetemCorrupt(BaseModel):
    percentage: int = Field(
        ..., ge=0, le=100, description="The corruption percentage between 0 and 100"
    )
    correlation: int = Field(
        ..., ge=0, le=100, description="The correlation percentage between 0 and 100"
    )
