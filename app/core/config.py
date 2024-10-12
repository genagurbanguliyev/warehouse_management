import os
from functools import lru_cache
from typing import List
from dotenv import load_dotenv
from pydantic.v1 import validator

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    ENV_STATE: str = "dev"

    def __init__(self, env_state: str, **kwargs):
        super().__init__(**kwargs)
        self.ENV_STATE = env_state

    PROJECT_NAME: str | None = "WarehouseManagement"
    PROJECT_ROOT: str = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    API: str = "/api"
    API_V1_STR: str = "/api/v1"
    DEFAULT_ADMIN: str = "admin"
    DEFAULT_ADMIN_PASSWORD: str = "admin123"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] | None = ["*"]

    # Cryption settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    JWT_SECRET: str

    # Time
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 15  # 12 hours

    # find query
    PAGE: int = 1
    PAGE_SIZE: int = 20
    ORDERING: str = "-id"

    # Database configurations
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    # For docker
    POSTGRES_DB: str = "postgres"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def parse_backend_cors_origins(cls, v):
        if isinstance(v, str):
            # Assuming the environment variable is a comma-separated string enclosed in square brackets
            if v.startswith("[") and v.endswith("]"):
                v = v[1:-1]  # Strip the enclosing brackets
            return [origin.strip("\"' ") for origin in v.split(",")]
        return v


class TESTSettings(BaseConfig):
    model_config = SettingsConfigDict(env_file=".env.test")


class DEVSettings(BaseConfig):
    model_config = SettingsConfigDict(env_file=".env.dev")


class PRODSettings(BaseConfig):
    model_config = SettingsConfigDict(env_file=".env.prod")


@lru_cache()
def get_config(env: str):
    match env:
        case "test":
            return TESTSettings(env)
        case "dev":
            return DEVSettings(env)
        case "prod":
            return PRODSettings(env)


load_dotenv()
environment = os.environ.get("ENVIRONMENT")
configs = get_config(environment)
