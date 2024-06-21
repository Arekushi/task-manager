from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html


async def redirect_to_docs(req: Request):
    return RedirectResponse(url='/docs')


async def get_swagger_ui(req: Request):
    return get_swagger_ui_html(
        openapi_url='/openapi.json',
        title='Swagger UI'
    )
