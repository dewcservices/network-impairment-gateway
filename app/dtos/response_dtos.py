from pydantic import BaseModel, Field


class Response(BaseModel):
    msg: str = Field(..., description="Request successful")
    isError: bool = Field(..., description="Did the request fail")
