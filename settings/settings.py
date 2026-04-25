from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    API_KEY: str
    BROKER_HOST: str
    BROKER_PORT: str
    BROKER_USER: str
    BROKER_PASS: str

    class Config:
        env_file = ".env"

    @property
    def db_url(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def broker_url(self):
        return (
            f"amqp://{self.BROKER_USER}:{self.BROKER_PASS}@"
            f"{self.BROKER_HOST}:{self.BROKER_PORT}/"
        )


settings = Settings()


@lru_cache()
def get_settings():
    return settings


SettingsDep = Annotated[Settings, Depends(get_settings)]
