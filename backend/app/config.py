"""Application configuration settings."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    whisper_model: str = "base"
    debug: bool = True

    class Config:
        """Pydantic configuration."""
        env_file = ".env"


# Global settings instance
settings = Settings()
