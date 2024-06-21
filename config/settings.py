from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    DATABASE_TYPE: str

    class Config:
        env_file = '.env'


settings = Settings()
