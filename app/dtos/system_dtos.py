from pydantic import BaseModel, Field


# what will happen is the bearer and environment settings will be combined to create a complete hbt and netem settings
class SystemStateDTO(BaseModel):
    bearer_id: int = Field(..., description="Bearer Profile Id")
    environment_id: int = Field(..., description="Environment Profile Id")

    class Config:
        from_attributes = True  # Equivalent to orm_mode
