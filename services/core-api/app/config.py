import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Vision Loop Core API (MongoDB)"
    ENVIRONMENT: str = "production"
    
    # MongoDB Unstructured Document Database
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017/visionloop_db")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "visionloop_db")
    
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    ZOHO_BOOKS_URL: str = os.getenv("ZOHO_BOOKS_URL", "http://zoho-connector:8001")
    AI_AGENT_URL: str = os.getenv("AI_AGENT_URL", "http://ai-agent-service:8002")
    TELEMATICS_URL: str = os.getenv("TELEMATICS_URL", "http://telematics-listener:8003")
    
    BASE_MONTHLY_RENT: float = 72000.00
    DEFAULT_GST_RATE: float = 18.00
    DEFAULT_SAC_CODE: str = "997311"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
