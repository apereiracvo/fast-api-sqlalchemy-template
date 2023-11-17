import os.path

from pydantic import BaseSettings
from sqlalchemy.engine.url import URL


class Settings(BaseSettings):
    # GENERAL CONFIG
    ROOT_PATH = os.path.dirname(__file__)  # ROOT = /app folder
    SERVICE_NAME: str = "sample-api"
    DEBUG: bool = False

    # DB CONNECTION CONFIG
    DB_DRIVER: str = "postgresql+asyncpg"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "password"
    DB_DATABASE: str = "postgres"

    # DB GENERAL CONFIG
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 0
    DB_ECHO: bool = False
    DB_AES_ENC_KEY: str = "some-secret-aes"

    # 3RD PARTY API CONFIGS
    OPENAI_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""

    @property
    def DB_DSN(self) -> URL:
        return URL.create(
            self.DB_DRIVER,
            self.DB_USER,
            self.DB_PASSWORD,
            self.DB_HOST,
            self.DB_PORT,
            self.DB_DATABASE,
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
print("----ENV DB Settings----")
print(f"DB_HOST: {settings.DB_HOST}")
print(f"DB_PORT: {settings.DB_PORT}")
