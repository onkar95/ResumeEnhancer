import json

from app.utils.json_utils import extract_json, parse_llm_json

from app.workflows.state import (
    ResumeTailorState
)

from app.schemas.resume import (
    ResumeDocument
)

from app.prompts.resume_tailor_prompt import (
    build_resume_tailor_prompt
)

from app.services import (
    LLMService
)


def resume_tailor_node(
    state: ResumeTailorState
):

    resume = state["parsed_resume"]

    jd = state["parsed_jd"]

    inventory = state.get(
        "resume_inventory"
    )

    approved_suggestions = state.get(
        "approved_suggestions"
    )

    enhancement_plan = state.get(
        "enhancement_plan"
    )

    tailoring_decision = state.get(
        "tailoring_decision"
    )
    user_context = state.get(
        "user_context"
    )

    prompt = build_resume_tailor_prompt(

        resume_json=resume.model_dump_json(
            indent=2
        ),

        job_description_json=jd.model_dump_json(
            indent=2
        ),

        inventory_json=(
            inventory.model_dump_json(
                indent=2
            )
            if inventory
            else "{}"
        ),

        approved_suggestions_json=(
            approved_suggestions
            .model_dump_json(
                indent=2
            )
            if approved_suggestions
            else "{}"
        ),

        enhancement_plan_json=(
            enhancement_plan
            .model_dump_json(
                indent=2
            )
            if enhancement_plan
            else "{}"
        ),

        tailoring_decision_json=(
            tailoring_decision
            .model_dump_json(
                indent=2
            )
            if tailoring_decision
            else "{}"
        ),
        user_context_json=(
            user_context
            .model_dump_json(
                indent=2
            )
            if user_context
            else "{}"
        )
    )

    llm = LLMService()

    # NOTE: intentionally NOT using a fixed-filename shortcut here anymore.
    # GroqService.generate() already caches by md5(prompt) under cache/
    # (see app/utils/llm_cache.py, gated by settings.DEBUG_USE_CACHE) --
    # so a truly-repeated resume+JD combo still skips the API call, but a
    # changed resume or JD always gets a fresh, correct tailored result.
    # A fixed-filename cache (the old approach) can't tell those apart and
    # will silently replay a stale resume tailored for different input.
    response = llm.generate(prompt)
    
    print("=" * 100)
    print("RAW GEMINI TAILOR RESPONSE")
    print(response)
    print("=" * 100)

    json_response = parse_llm_json(response)

    tailored_resume = (
        ResumeDocument
        .model_validate(
            json_response
        )
    )

    tailored_resume.contact_info.github_url = resume.contact_info.github_url
    tailored_resume.contact_info.linkedin_url = resume.contact_info.linkedin_url
    tailored_resume.contact_info.portfolio_url = resume.contact_info.portfolio_url
    tailored_resume.contact_info.website_url = resume.contact_info.website_url

    return {
        "tailored_resume":
            tailored_resume
    }

