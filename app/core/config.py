import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # API Settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    MONGODB_URL: str = os.getenv("MONGODB_URL", "")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "relaii")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Email Settings
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_SSL: bool = os.getenv("SMTP_SSL", "False").lower() == "true"
    EMAIL_FROM_NAME: str = os.getenv("EMAIL_FROM_NAME", "Relaii Team")
    EMAIL_FROM_ADDRESS: str = os.getenv("EMAIL_FROM_ADDRESS", "")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

    # Resend API Key
    RESEND_API_KEY: str = os.getenv("RESEND_API_KEY", "")

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()