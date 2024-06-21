from fastapi import HTTPException
from fastapi.responses import JSONResponse


async def general_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            'message': 'An unexpected error occurred'
        }
    )


async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'message': str(exc.detail)
        }
    )
