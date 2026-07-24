import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ForgeAI Multi-Agent Engine"
    API_V1_STR: str = "/api/v1"
    
    # AI Providers
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    DEEPSEEK_API_KEY: Optional[str] = None
    GOOGLE_GEMINI_API_KEY: Optional[str] = None
    TAVILY_API_KEY: Optional[str] = None
    
    # Provider Model Overrides
    OPENAI_MODEL: str = "gpt-4o"
    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-20241022"
    DEEPSEEK_MODEL: str = "deepseek-coder"
    GEMINI_MODEL: str = "gemini-1.5-pro"
    
    # Auth
    FIREBASE_PROJECT_ID: Optional[str] = None
    FIREBASE_CLIENT_EMAIL: Optional[str] = None
    FIREBASE_PRIVATE_KEY: Optional[str] = None
    JWT_SECRET: str = "default-insecure-forgeai-secret-key-32chars"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Infrastructure
    DATABASE_URL: str = "sqlite+aiosqlite:///./forgeai.db"
    DATABASE_URL_SYNC: str = "sqlite:///./forgeai.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Sandbox
    SANDBOX_WORKSPACE_DIR: str = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "sandbox", "workspace")
    )
    MAX_DEBUG_RETRIES: int = 3
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
