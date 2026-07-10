from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Resume Tailor AI"

    # Groq
    GROQ_API_KEY: str="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" 
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    # GROQ_MODEL: str = "llama-3.1-8b-instant"

    class Config:
        env_file = ".env"

    OPENAI_API_KEY: str 
    OPENAI_MODEL: str = 'gpt-4.1-mini'


settings = Settings()
