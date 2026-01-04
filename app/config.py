from typing import List, Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "beaver"
    ENV: str = "dev"

    # Database Configuration
    DATABASE_URL: Optional[str] = None  # If not set, defaults to SQLite
    # For PostgreSQL: postgresql+psycopg2://user:password@localhost/dbname
    # For SQLite: sqlite:///./beaver.db (default)

    REDIS_URL: str

    # Provider API Keys
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    DEEPSEEK_API_KEY: str = ""
    PERPLEXITY_API_KEY: str = ""
    XAI_API_KEY: str = ""

    # CORS Settings
    FRONTEND_URL: str = "https://beaver-ai-hub.lovable.app"
    CORS_ORIGINS: List[str] = [
        "https://beaver-ai-hub.lovable.app",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
    ]

    # JWT Settings
    JWT_SECRET: str = ""  # Must be set in .env (use: openssl rand -hex 32)
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
