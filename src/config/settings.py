"""Configuration settings for the Financial Agent."""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    LOGS_DIR: Path = BASE_DIR / "logs"
    
    # HuggingFace
    HF_TOKEN: Optional[str] = None
    HF_MODEL: str = "meta-llama/Llama-3.1-8B-Instruct"
    
    # Database
    DATABASE_URL: str = "sqlite:///./data/financial_agent.db"
    
    # Agent Configuration
    MAX_STEPS: int = 10
    DEFAULT_PERIOD: str = "1mo"
    CACHE_EXPIRY_MINUTES: int = 15
    
    # Alerts
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_CHAT_ID: Optional[str] = None
    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_EMAIL: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create directories if they don't exist
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Global settings instance
settings = Settings()
