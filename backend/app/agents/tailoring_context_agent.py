from app.workflows.state import (
    ResumeTailorState
)

from app.schemas.tailoring_context import (
    TailoringContext
)


def tailoring_context_node(
    state: ResumeTailorState
):

    plan = state[
        "enhancement_plan"
    ]

    context = TailoringContext(

        skills_to_add=
            plan.skills_to_add,

        skills_to_emphasize=
            plan.skills_to_emphasize,

        keyword_targets=
            plan.keyword_targets
    )

    return {
        "tailoring_context":
            context
    }