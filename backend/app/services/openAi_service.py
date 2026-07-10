from openai import AsyncOpenAI

from app.core.config import settings


class OpenAIService:

    def __init__(self):

        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY
        )

        self.model = settings.OPENAI_MODEL

    async def generate(
        self,
        prompt: str,
        temperature: float = 0.1,
        max_tokens: int = 4096,
    ) -> str:

        try:

            response = await self.client.chat.completions.create(
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

            return (
                response
                .choices[0]
                .message
                .content
                or ""
            )

        except Exception as exc:

            raise Exception(
                f"OpenAI Error: {exc}"
            ) from exc

    async def generate_json(
        self,
        prompt: str,
    ) -> str:

        system_prompt = """
You are a JSON API.

Return ONLY valid JSON.

Do NOT return markdown.

Do NOT explain anything.

Return JSON only.
"""

        try:

            response = await self.client.chat.completions.create(
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

            return (
                response
                .choices[0]
                .message
                .content
                or ""
            )

        except Exception as exc:

            raise Exception(
                f"OpenAI JSON Error: {exc}"
            ) from exc