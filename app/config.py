from typing import Literal
from pydantic import  ConfigDict, model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_NAME: str
    DB_PASS: str
    DATABASE_URL: str = ""

    REDIS_HOST: str
    REDIS_PORT: int

    @model_validator(mode='after')
    def get_database_url(cls, values):
        values.DATABASE_URL = (
            f"postgresql+asyncpg://{values.DB_USER}:{values.DB_PASS}@{values.DB_HOST}:{values.DB_PORT}/{values.DB_NAME}"
        )
        return values

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_NAME: str
    TEST_DB_PASS: str
    TEST_DATABASE_URL: str = ""

    @model_validator(mode='after')
    def get_test_database_url(cls, values):
        values.TEST_DATABASE_URL = (
            f"postgresql+asyncpg://{values.TEST_DB_USER}:{values.TEST_DB_PASS}@{values.TEST_DB_HOST}:{values.TEST_DB_PORT}/{values.TEST_DB_NAME}"
        )
        return values

    model_config = ConfigDict(
        env_file=".env",
    )


settings = Settings()
