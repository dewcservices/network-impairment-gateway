from fastapi import Request
from fastapi.responses import JSONResponse

from app.dtos.response_dtos import ResponseDTO


class RequestProcessingException(Exception):
    def __init__(self, status_code: int, detail: str, stack_trace: str = ""):
        self.status_code = status_code
        self.detail = detail
        self.stack_trace = stack_trace


async def request_processing_exception_handler(
    request: Request, exc: RequestProcessingException
):

    return JSONResponse(
        status_code=exc.status_code,
        content=ResponseDTO(isError=True, msg=exc.detail).model_dump(),
    )
