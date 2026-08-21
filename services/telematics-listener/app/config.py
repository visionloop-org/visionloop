import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Vision Loop Telematics Ingestor"
    CORE_API_URL: str = os.getenv("CORE_API_URL", "http://core-api:8000")
    SIMULATION_INTERVAL_SEC: int = int(os.getenv("SIMULATION_INTERVAL_SEC", "5"))

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
