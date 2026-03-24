"""
Configuration management for Scripture AI
Load settings from .env file
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings loaded from .env"""
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:grace123@localhost:5432/scripture_db"
    )
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    ENV: str = os.getenv("ENV", "development")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
    )
    
    # Files
    KJV_PLUS_FILE: str = os.getenv("KJV_PLUS_FILE", "kjv_with_strongs.json")
    
    def __repr__(self) -> str:
        return f"<Settings ENV={self.ENV} DB={self.DATABASE_URL}>"

# Create settings instance
settings = Settings()
