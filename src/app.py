from config import dynaconf_settings as settings
from fastapi import FastAPI, HTTPException

from src.redirects import get_swagger_ui, redirect_to_docs
from src.exception_handlers import general_exception_handler, http_exception_handler
from src.controllers.task_controller import task_router

def create_app() -> FastAPI:    
    app = FastAPI(
        title=settings.app.title,
        description=settings.app.description,
        version=settings.app.version,
        openapi_url=settings.app.openapi_url,
        contact=settings.app.contact,
        servers=settings.app.servers
    )
    
    add_routers(app)
    add_exception_handlers(app)
    add_redirections(app)

    return app


def add_exception_handlers(app: FastAPI):
    for exception, function in [
        (Exception, general_exception_handler),
        (HTTPException, http_exception_handler)
    ]:
        app.add_exception_handler(exception, function)


def add_redirections(app: FastAPI):
    for path, callback, methods in [
        ('/', redirect_to_docs, ['GET']),
        ('/docs', get_swagger_ui, ['GET'])
    ]:
        app.add_route(path, callback, methods)


def add_routers(app: FastAPI):
    for router in [
        task_router
    ]:
        app.include_router(router)
