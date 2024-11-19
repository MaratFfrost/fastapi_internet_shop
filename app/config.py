from typing import Literal
from pydantic import BaseModel, Field, ConfigDict, model_validator
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

    SECRET_KEY: str
    SECRET_ALGORITHM: str

    RABBITMQ_HOST: str
    RABBITMQ_PORT: int

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_PORT: int

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_NAME: str
    TEST_DB_PASS: str
    TEST_DATABASE_URL: str = ""

    @model_validator(mode='after')
    def generate_database_urls(self):
        self.DATABASE_URL = (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
        self.TEST_DATABASE_URL = (
            f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
        )
        return self

    model_config = ConfigDict(
        env_file=".env",
    )


settings = Settings()
