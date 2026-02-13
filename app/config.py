from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Business Analyst Platform"

    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    # LLM Keys
    OPENAI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None

    # LLM Model
    GROQ_MODEL: str = "llama3-8b-8192"

    model_config = ConfigDict(
        env_file=".env",
        extra="allow",
    )


settings = Settings()
