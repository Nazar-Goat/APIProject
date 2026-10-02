from typing import Literal

from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENVIRONMENT: Literal["DEV", "PROD"]

    APP_NAME: str
    APP_PORT: int

    MONGO_URI: str
    MONGO_DB_NAME: str

    MONGO_MAX_POOL_SIZE: int = 50
    MONGO_MIN_POOL_SIZE: int = 10

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASS: str
    REDIS_AUTH_DB: str
    REDIS_THROTTLING_DB: str
    REDIS_QUEUE_DB: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    FAILED_LOGIN_ATTEMPTS: int
    FAILED_LOGIN_ATTEMPTS_TIMEOUT: int

    REFRESH_TTL_DAYS: int
    ACCESS_TTL_MINUTES: int
    ACCESS_COOKIE_NAME: str = "access_token"
    REFRESH_COOKIE_NAME: str = "refresh_token"

    WSS_TOKEN_TTL: int = 30

    model_config = SettingsConfigDict(env_file=find_dotenv())

settings = Settings()