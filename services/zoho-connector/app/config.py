import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Vision Loop Zoho Connector"
    CORE_API_URL: str = os.getenv("CORE_API_URL", "http://core-api:8000")
    
    # Zoho Books API Credentials
    ZOHO_CLIENT_ID: str = os.getenv("ZOHO_CLIENT_ID", "")
    ZOHO_CLIENT_SECRET: str = os.getenv("ZOHO_CLIENT_SECRET", "")
    ZOHO_REFRESH_TOKEN: str = os.getenv("ZOHO_REFRESH_TOKEN", "")
    ZOHO_ORG_ID: str = os.getenv("ZOHO_ORG_ID", "")
    ZOHO_API_DOMAIN: str = os.getenv("ZOHO_API_DOMAIN", "https://books.zoho.in/api/v3")
    ZOHO_ACCOUNTS_DOMAIN: str = os.getenv("ZOHO_ACCOUNTS_DOMAIN", "https://accounts.zoho.in")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
