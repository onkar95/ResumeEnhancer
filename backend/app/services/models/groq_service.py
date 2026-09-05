"""
Groq Service

Centralized Groq client used by all AI services.

Responsibilities:
- Create Groq client
- Send prompts
- Return model responses
- Handle API errors

Author: Resume Tailor AI
"""

from groq import Groq
from groq import (
    APIConnectionError,
    APIStatusError,
    RateLimitError,
)

from app.core.config import settings
from langsmith import traceable

from app.utils.llm_cache import (
    build_cache_key,
    load_cache,
    save_cache,
)


class GroqService:
    """
    Wrapper around Groq Chat Completions API.
    """

    def __init__(self) -> None:
        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

        self.model = settings.GROQ_MODEL

    @traceable(name="groq_generate")
    def generate(
        self,
        prompt: str,
        temperature: float = 0.1,
        max_tokens: int = 4096,
    ) -> str:

        cache_key = build_cache_key(
            prompt,
            prefix="generate"
        )

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

            response = self.client.chat.completions.create(
                model=self.model,
                temperature=temperature,
                max_tokens=max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            content = (
                response.choices[0]
                .message.content
                or ""
            )

            if settings.DEBUG_USE_CACHE:

                save_cache(
                    cache_key,
                    {
                        "response": content
                    }
                )

            return content

        except RateLimitError as exc:
            raise Exception(
                "Groq rate limit exceeded."
            ) from exc

        except APIConnectionError as exc:
            raise Exception(
                "Unable to connect to Groq."
            ) from exc

        except APIStatusError as exc:
            raise Exception(
                f"Groq API Error: {exc}"
            ) from exc

        except Exception as exc:
            raise Exception(
                f"Unexpected Groq Error: {exc}"
            ) from exc

    @traceable(name="groq_generate_json")
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
            prefix="generate_json"
        )

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

            response = self.client.chat.completions.create(
                model=self.model,
                temperature=0.1,
                response_format={
                    "type": "json_object"
                },
                # max_tokens=8192,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            )

            content = (
                response.choices[0]
                .message.content
                or ""
            )

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
                f"Groq JSON Error: {exc}"
            ) from exc

