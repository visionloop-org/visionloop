import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Vision Loop Telegram Bot"
    CORE_API_URL: str = os.getenv("CORE_API_URL", "http://core-api:8000")
    AI_AGENT_URL: str = os.getenv("AI_AGENT_URL", "http://ai-agent-service:8002")
    
    # Telegram Bot Credentials
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_ADMIN_CHAT_ID: str = os.getenv("TELEGRAM_ADMIN_CHAT_ID", "")
    WEBHOOK_DOMAIN: str = os.getenv("TELEGRAM_WEBHOOK_DOMAIN", "")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
