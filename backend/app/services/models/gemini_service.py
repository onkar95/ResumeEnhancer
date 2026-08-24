"""
Gemini Service

Centralized Gemini client used by all AI services.

Responsibilities:
- Create Gemini client
- Send prompts
- Return model responses
- Handle API errors
- Cache responses during development

Author: Resume Tailor AI
"""

from google import genai
from google.genai import types

from app.core.config import settings
from langsmith import traceable

from app.utils.llm_cache import (
    build_cache_key,
    load_cache,
    save_cache,
)


class GeminiService:
    """
    Wrapper around Google Gemini API.
    """

    def __init__(self) -> None:

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = settings.GEMINI_MODEL

    # ---------------------------------------------------------
    # Normal text generation
    # ---------------------------------------------------------

    @traceable(name="gemini_generate")
    def generate(
        self,
        prompt: str,
        temperature: float = 0.1,
        max_tokens: int = 16348,
    ) -> str:

        cache_key = build_cache_key(
            prompt,
            prefix="gemini_generate"
        )

        # -----------------------------------------------------
        # Cache
        # -----------------------------------------------------

        if settings.DEBUG_USE_CACHE:

            cached = load_cache(
                cache_key
            )

            if cached:

                print(
                    f"[CACHE HIT] {cache_key}"
                )

                return cached["response"]

        try:

            print(
                f"[CACHE MISS] {cache_key}"
            )

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                ),
            )

            content = response.text or ""

            # -------------------------------------------------
            # Save cache
            # -------------------------------------------------

            if settings.DEBUG_USE_CACHE:

                save_cache(
                    cache_key,
                    {
                        "response": content
                    }
                )

            return content

        except Exception as exc:

            raise Exception(
                f"Gemini API Error: {exc}"
            ) from exc

    # ---------------------------------------------------------
    # JSON generation
    # ---------------------------------------------------------

    @traceable(name="gemini_generate_json")
    async def generate_json(
        self,
        prompt: str,
    ) -> str:

        system_prompt = """
You are a JSON API.

Return ONLY valid JSON.

Do NOT return markdown.

Do NOT use ```json.

Do NOT explain anything.

Return JSON only.
"""

        cache_key = build_cache_key(
            prompt,
            prefix="gemini_generate_json"
        )

        # -----------------------------------------------------
        # Cache
        # -----------------------------------------------------

        if settings.DEBUG_USE_CACHE:

            cached = load_cache(
                cache_key
            )

            if cached:

                print(
                    f"[CACHE HIT] {cache_key}"
                )

                return cached["response"]

        try:

            print(
                f"[CACHE MISS] {cache_key}"
            )

            full_prompt = (
                system_prompt
                + "\n\n"
                + prompt
            )

            response = self.client.models.generate_content(
                model=self.model,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    response_mime_type="application/json",
                ),
            )

            content = response.text or ""

            # -------------------------------------------------
            # Save cache
            # -------------------------------------------------

            if settings.DEBUG_USE_CACHE:

                save_cache(
                    cache_key,
                    {
                        "response": content
                    }
                )

            return content

        except Exception as exc:

            raise Exception(
                f"Gemini JSON Error: {exc}"
            ) from exc