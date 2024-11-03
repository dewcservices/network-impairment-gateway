from pydantic import BaseModel, Field


# what will happen is the bearer and environment settings will be combined to create a complete hbt and netem settings
class SystemStateDTO(BaseModel):
    bearer_id: int = Field(..., description="Bearer Profile Id")
    uplink_environment_id: int = Field(..., description="Uplink Environment Profile Id")
    downlink_environment_id: int = Field(
        ..., description="Downlink Environment Profile Id"
    )

    class ConfigDict:
        from_attributes = True  # Equivalent to orm_mode
