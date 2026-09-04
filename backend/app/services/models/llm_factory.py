# services/llm_factory.py
from app.core.config import settings
from app.services.models.gemini_service import GeminiService
from app.services.models.groq_service import GroqService
from app.services.models.openAi_service import OpenAIService


def get_llm_service():
    if settings.LLM_PROVIDER == "groq":
        return GroqService()
    if settings.LLM_PROVIDER == "openai":
        return OpenAIService()
    return GeminiService()
