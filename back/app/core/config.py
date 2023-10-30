from typing import List
from decouple import config
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings
"""
This module defines the application's configuration settings using environment variables and default values.
"""

class Settings(BaseSettings):
    API_V1_STR: str = "/api"
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", cast=str)
    JWT_REFRESH_SECRET_KEY: str = config("JWT_REFRESH_SECRET_KEY", cast=str)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7   # 7 days
    BACKEND_CORS_ORIGINS: str = "http://localhost:5173"
    PROJECT_NAME: str = "Café Sans Fil"
    
    # Database
    MONGO_CONNECTION_STRING: str = config("MONGO_CONNECTION_STRING", cast=str)
    
    class Config:
        case_sensitive = True
        
settings = Settings()
