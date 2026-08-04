import json

from app.utils.json_utils import extract_json

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

    json_response = extract_json(response)

    tailored_resume = (
        ResumeDocument
        .model_validate(
            json_response
        )
    )

    return {

        "tailored_resume":
            tailored_resume
    }

# import json
# from pathlib import Path

# from app.utils.json_utils import extract_json

# from app.workflows.state import (
#     ResumeTailorState
# )

# from app.schemas.resume import (
#     ResumeDocument
# )

# from app.prompts.resume_tailor_prompt import (
#     build_resume_tailor_prompt
# )

# from app.services import (
#     LLMService
# )
# from typing import Any


# def resume_tailor_node(
#     state: ResumeTailorState
# ):

#     resume = state["parsed_resume"]

#     jd = state["parsed_jd"]

#     inventory = state.get(
#         "resume_inventory"
#     )

#     approved_suggestions = state.get(
#         "approved_suggestions"
#     )

#     enhancement_plan = state.get(
#         "enhancement_plan"
#     )

#     tailoring_decision = state.get(
#         "tailoring_decision"
#     )

#     prompt = build_resume_tailor_prompt(

#         resume_json=resume.model_dump_json(
#             indent=2
#         ),

#         job_description_json=jd.model_dump_json(
#             indent=2
#         ),

#         inventory_json=(
#             inventory.model_dump_json(
#                 indent=2
#             )
#             if inventory
#             else "{}"
#         ),

#         approved_suggestions_json=(
#             approved_suggestions
#             .model_dump_json(
#                 indent=2
#             )
#             if approved_suggestions
#             else "{}"
#         ),

#         enhancement_plan_json=(
#             enhancement_plan
#             .model_dump_json(
#                 indent=2
#             )
#             if enhancement_plan
#             else "{}"
#         ),

#         tailoring_decision_json=(
#             tailoring_decision
#             .model_dump_json(
#                 indent=2
#             )
#             if tailoring_decision
#             else "{}"
#         )
#     )

#     llm = LLMService()

#     file_path = Path("app/data/llm_response.txt")

#     savedResponse: str = ""

#     if file_path.exists():
#         with open(file_path, "r", encoding="utf-8") as f:
#             savedResponse = f.read()

#     if savedResponse.strip():
#         print("Using saved response")
#         response = savedResponse

#     else:
#         print("Calling LLM")
#         response = llm.generate(prompt)

#         file_path.parent.mkdir(parents=True, exist_ok=True)

#         with open(file_path, "w", encoding="utf-8") as f:
#             f.write(response)

#     # response = llm.generate(
#     #         prompt
#     #     )

#     print("response=" * 100)
#     print(json.dumps(response, indent=2))
#     print("=" * 100)

#     json_response = extract_json(response)

#     print("json_response=" * 100)
#     print(json.dumps(json_response, indent=2))
#     print("=" * 100)

#     tailored_resume = (
#         ResumeDocument
#         .model_validate(
#             json_response
#         )
#     )

#     return {

#         "tailored_resume":
#             tailored_resume
#     }
