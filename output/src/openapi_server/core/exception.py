from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from .response import error

class APIException(Exception):
    def __init__(self, msg: str = "API error", code: int = 1, data: any = None, status_code: int = 200):
        self.msg = msg
        self.code = code
        self.data = data
        self.status_code = status_code

async def api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(status_code=exc.status_code, content=error(msg=exc.msg, code=exc.code, data=exc.data))

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content=error(msg=exc.detail, code=exc.status_code))

async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content=error(msg=str(exc), code=500)) 