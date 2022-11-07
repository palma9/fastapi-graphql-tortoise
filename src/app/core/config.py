import os

from pydantic import BaseSettings


class __Settings(BaseSettings):

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    # Database
    DB_HOST: str = os.environ.get("DB_HOST", "database")
    DB_PORT: int = os.environ.get("DB_PORT", 5432)
    DB_USER: str = os.environ.get("DB_USER", "postgres")
    DB_PASSWORD: str = os.environ.get("DB_PASSWORD", "postgres")
    DB_NAME: str = os.environ.get("DB_NAME", "postgres")

    # Auth
    JWT_SECRET: str = os.environ.get("JWT_SECRET", "superSecret!")
    ALGORITHM: str = os.environ.get("ALGORITHM", "HS256")
    APPLE_CLIENT_ID: str = os.environ.get("APPLE_CLIENT_ID", None)

    # Redis
    REDIS_HOST: str = os.environ.get("REDIS_HOST", "redis")
    REDIS_PORT: int = os.environ.get("REDIS_PORT", 6379)

    # Broadcast
    BROADCAST_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"


settings = __Settings()
