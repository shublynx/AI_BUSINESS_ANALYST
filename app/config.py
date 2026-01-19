"""
Central configuration module.
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Business Analyst Platform"

    class Config:
        env_file = ".env"

settings = Settings()
