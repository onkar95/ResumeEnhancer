from app.core.logger import logger
from app.services.groq_service import GroqService as LLMService
from app.utils.json_utils import extract_json
from app.schemas.user_context import UserContext, DeclaredSkill
from app.prompts.user_context_prompt import build_user_context_prompt
from app.workflows.state import ResumeTailorState


async def user_context_node(state: ResumeTailorState):
    """
    Optional step. If the candidate left the "additional comments" box
    empty, this is a no-op that returns an empty UserContext -- the rest
    of the pipeline behaves exactly as before.
    """

    instructions = (state.get("user_instructions") or "").strip()

    if not instructions:
        logger.info(
            "No user instructions provided; skipping user_context extraction"
        )
        return {"user_context": UserContext(raw_instructions="")}

    logger.info("started user_context_agent")

    llm = LLMService()

    try:
        prompt = build_user_context_prompt(instructions)

        response = await llm.generate_json(prompt)

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

        context = UserContext(
            raw_instructions=instructions,
            declared_skills=declared_skills,
            tailoring_mode=parsed.get("tailoring_mode"),
        )

        logger.info("user_context=%s", context.model_dump())

    except Exception:
        # Extraction failing should never break the workflow -- fall back
        # to just carrying the raw text forward so the tailor prompt can
        # still see it verbatim.
        logger.exception(
            "Failed to parse user instructions; falling back to raw text only"
        )
        context = UserContext(raw_instructions=instructions)

    return {"user_context": context}