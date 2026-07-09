"""Settings and Configuration."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    GCP_PROJECT_ID: str = "demo-project"
    GCP_REGION: str = "us-central1"
    GEMINI_MODEL: str = "gemini-2.5-pro"
    FIRESTORE_DATABASE: str = "(default)"
    BACKEND_ENV: str = "development"
    BACKEND_PORT: int = 8080
    BACKEND_CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    BACKEND_RATE_LIMIT: str = "100/minute"
    SECRET_KEY: str = "demo-secret-key-must-be-32-bytes-long!"
    ENABLE_SIMULATION: bool = True
    ENABLE_AI: bool = True
    BACKEND_LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",")]

settings = Settings()
