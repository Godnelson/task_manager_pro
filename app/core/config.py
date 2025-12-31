from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Task Manager Pro"
    env: str = "dev"

    cors_origins: str = "*"
    jwt_secret: str = "CHANGE_ME"
    jwt_alg: str = "HS256"
    access_token_expire_min: int = 15
    refresh_token_expire_days: int = 14
    refresh_token_pepper: str = "CHANGE_ME_PEPPER"

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/taskdb"

    @field_validator("cors_origins")
    @classmethod
    def _cors(cls, v: str) -> str:
        return v

    def cors_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

settings = Settings()
