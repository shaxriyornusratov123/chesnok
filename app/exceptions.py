from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import status


class NimadirException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


async def zero_devision_error_exc(request: Request, exc: ZeroDivisionError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"message": exc.args[0]}
    )


async def nimadir_error_exc(request: Request, exc: NimadirException):
    return JSONResponse(
        status_code=status.HTTP_406_NOT_ACCEPTABLE, content={"message": exc.msg}
    )
