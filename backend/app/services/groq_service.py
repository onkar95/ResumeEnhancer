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


class GroqService:
    """
    Wrapper around Groq Chat Completions API.
    """

    def __init__(self) -> None:
        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

        self.model = settings.GROQ_MODEL

    def generate(
        self,
        prompt: str,
        temperature: float = 0.1,
        max_tokens: int = 4096,
    ) -> str:
        """
        Generate response from Groq.

        Args:
            prompt: Complete prompt
            temperature: Sampling temperature
            max_tokens: Maximum output tokens

        Returns:
            Raw LLM response string.
        """

        try:

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

            return response.choices[0].message.content or ""

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

    async def generate_json(
        self,
        prompt: str,
    ) -> str:
        """
        Helper specifically for JSON responses.
        """

        system_prompt = """
You are a JSON API.

Return ONLY valid JSON.

Do NOT return markdown.

Do NOT use ```json.

Do NOT explain anything.

Return JSON only.
"""

        try:

            response = self.client.chat.completions.create(
                model=self.model,
                temperature=0.1,
                response_format={
                    "type": "json_object"
                },
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

            return response.choices[0].message.content or ""

        except Exception as exc:
            raise Exception(
                f"Groq JSON Error: {exc}"
            ) from exc

# from groq import Groq

# from app.core.config import settings


# class GroqService:

#     def __init__(self):
#         self.client = Groq(
#             api_key=settings.GROQ_API_KEY
#         )

#     async def generate(
#         self,
#         prompt: str
#     ):

#         response = self.client.chat.completions.create(
#             model=settings.GROQ_MODEL,
#             messages=[
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ]
#         )

#         return response.choices[0].message.content
