from typing import List
from decouple import config
from pydantic_settings import SettingsConfigDict, BaseSettings

"""
This module defines the application's configuration settings using environment variables and default values.
"""


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)
    API_V1_STR: str = "/api"
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", cast=str)
    JWT_REFRESH_SECRET_KEY: str = config("JWT_REFRESH_SECRET_KEY", cast=str)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    BACKEND_CORS_ORIGINS: List[str] = config(
        "BACKEND_CORS_ORIGINS", cast=lambda v: v.split(",")
    )
    BASE_URL: str = config("BASE_URL", cast=str)
    PROJECT_NAME: str = "Café sans-fil"
    VERSION: str = "0.2.0"

    # Database
    MONGO_CONNECTION_STRING: str = config("MONGO_CONNECTION_STRING", cast=str)
    MONGO_DB_NAME: str = config("MONGO_DB_NAME", cast=str)

    # Mail
    SENDGRID_API_KEY: str = config("SENDGRID_API_KEY", cast=str)
    # Disable email sending because of Render blocking SMTP requests
    # MAIL_USERNAME: str = config("MAIL_USERNAME", cast=str)
    # MAIL_PASSWORD: str = config("MAIL_PASSWORD", cast=str)
    # MAIL_FROM: str = config("MAIL_FROM", cast=str)
    # MAIL_PORT: int = config("MAIL_PORT", cast=int)
    # MAIL_SERVER: str = config("MAIL_SERVER", cast=str)
    # MAIL_FROM_NAME: str = config("MAIL_FROM_NAME", cast=str)


settings = Settings()
