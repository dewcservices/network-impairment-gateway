from pydantic import BaseModel, Field


class ResponseDTO(BaseModel):
    msg: str = Field(..., description="Request successful")
    isError: bool = Field(..., description="Did the request fail")
