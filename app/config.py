from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "Complaint Management System"
    DEBUG: bool = False
    DATA_FILE: str = "data/complaints.json"
    AUTH_REQUIRED: bool = False
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "secret"
    CORS_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()