"""
Sync extraction of structured UserContext from free-form candidate notes.

Used both by the initial workflow (user_context_agent, wrapping this) and
by the chat-revise endpoint (which is a sync FastAPI route and can't await
GroqService.generate_json directly).
"""

# from ResumeEnhancer.backend.app.services.models.groq_service import GroqService
from app.services.models.gemini_service import GeminiService
from app.utils.json_utils import extract_json
from app.schemas.user_context import UserContext, DeclaredSkill
from app.prompts.user_context_prompt import build_user_context_prompt
from app.core.logger import logger


def extract_user_context(instructions: str) -> UserContext:

    instructions = (instructions or "").strip()

    if not instructions:
        return UserContext(raw_instructions="")

    llm = GeminiService()

    try:
        prompt = build_user_context_prompt(instructions)

        response = llm.generate(prompt)

        parsed = extract_json(response)

        declared_skills = [
            DeclaredSkill(
                skill=item.get("skill", "").strip(),
                confidence=float(item.get("confidence") or 0.6),
                note=item.get("note"),
            )
            for item in parsed.get("declared_skills", [])
            if item.get("skill", "").strip()
        ]

        return UserContext(
            raw_instructions=instructions,
            declared_skills=declared_skills,
            tailoring_mode=parsed.get("tailoring_mode"),
        )

    except Exception:
        logger.exception(
            "Failed to extract user context; falling back to raw text only"
        )
        return UserContext(raw_instructions=instructions)