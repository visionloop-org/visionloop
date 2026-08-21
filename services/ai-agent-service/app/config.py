import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Vision Loop AI Multi-Agent Service"
    CORE_API_URL: str = os.getenv("CORE_API_URL", "http://core-api:8000")
    ZOHO_BOOKS_URL: str = os.getenv("ZOHO_BOOKS_URL", "http://zoho-connector:8001")
    
    # LLM Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    AI_MODEL_NAME: str = os.getenv("AI_MODEL_NAME", "gemini-2.0-flash")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
