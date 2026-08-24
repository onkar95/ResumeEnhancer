from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "Resume Tailor AI"

    # Groq
    GROQ_API_KEY: str
    # GROQ_MODEL: str = "llama-3.3-70b-versatile"
    # GROQ_MODEL: str = "llama-3.1-8b-instant"
    GROQ_MODEL: str
    DEBUG_USE_CACHE: bool = True


    GEMINI_MODEL: str
    GEMINI_API_KEY: str

    # class Config:
    #     env_file = ".env"

    OPENAI_API_KEY: str
    OPENAI_MODEL: str = 'gpt-4.1-mini'

    LANGSMITH_TRACING: str
    LANGSMITH_ENDPOINT: str
    LANGSMITH_API_KEY: str
    LANGSMITH_PROJECT: str

    # MongoDB
    MONGO_URI: str
    MONGO_DB_NAME: str

    # Google OAuth
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/callback"

    # Sessions / JWT
    SESSION_SECRET_KEY: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    FRONTEND_URL: str = "http://localhost:5173"
    COOKIE_SECURE: bool = False  # True in production (HTTPS)

    # Modern Pydantic V2 Configuration Block
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # Softly ignores tracking parameters LangGraph extracts directly
    )


settings = Settings()
