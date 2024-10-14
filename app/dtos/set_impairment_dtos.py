from pydantic import BaseModel, Field


# what will happen is the bearer and environment settings will be combined to create a complete hbt and netem settings
class SetImpairmentDTO(BaseModel):
    bearer_id: int = Field(..., description="Bearer Profile Id")
    environment_id: int = Field(..., description="Environment Profile Id")
