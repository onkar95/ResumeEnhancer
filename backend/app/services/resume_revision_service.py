"""
Resume Revision Service

Reusable "call the tailor LLM again" function, used by the human-review
/revise endpoint. Deliberately separate from resume_tailor_agent.py's graph
node, which uses the single-file app/data/llm_response.txt shortcut on
purpose (kept as-is per product decision to conserve Groq quota during
initial-run iteration).

This service instead relies on GroqService.generate()'s own prompt-hash
cache (app/utils/llm_cache.py, keyed by md5 of the prompt) -- appropriate
here since every revise call has genuinely different content (different
approved suggestions / edits), so there's no single "the" response to pin.
"""

from app.prompts.resume_tailor_prompt import build_resume_tailor_prompt
from app.schemas.resume import ResumeDocument
from app.services.groq_service import GroqService
from app.utils.json_utils import extract_json
from app.utils.resume_normalizer import normalize_resume


def regenerate_tailored_resume(
    resume_json: str,
    job_description_json: str,
    inventory_json: str,
    approved_suggestions_json: str,
    enhancement_plan_json: str,
    tailoring_decision_json: str = "{}",
) -> ResumeDocument:

    prompt = build_resume_tailor_prompt(
        resume_json=resume_json,
        job_description_json=job_description_json,
        inventory_json=inventory_json,
        approved_suggestions_json=approved_suggestions_json,
        enhancement_plan_json=enhancement_plan_json,
        tailoring_decision_json=tailoring_decision_json,
    )

    llm = GroqService()

    response = llm.generate(prompt)

    parsed_json = extract_json(response)

    normalized = normalize_resume(parsed_json)

    return ResumeDocument.model_validate(normalized)
