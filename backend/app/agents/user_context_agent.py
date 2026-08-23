from app.core.logger import logger
from app.schemas.user_context import UserContext
from app.services.user_context_service import extract_user_context
from app.workflows.state import ResumeTailorState


def user_context_node(state: ResumeTailorState):
    """
    Optional step. If the candidate left the notes box empty, this is a
    no-op -- the rest of the pipeline behaves exactly as before.
    """

    instructions = (state.get("user_instructions") or "").strip()

    if not instructions:
        logger.info("No user instructions provided; skipping user_context extraction")
        return {"user_context": UserContext(raw_instructions="")}

    logger.info("started user_context_agent")

    context = extract_user_context(instructions)

    logger.info("user_context=%s", context.model_dump())

    return {"user_context": context}