import uvicorn

from config import dynaconf_settings as settings
from src.app import create_app


app = create_app()


def main():
    uvicorn.run(
        'main:app',
        host=settings.HOST_URL,
        port=settings.HOST_PORT,
        reload=bool(settings.RELOAD)
    )


if __name__ == '__main__':
    main()
