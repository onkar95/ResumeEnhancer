from app.workflows.state import (
    ResumeTailorState
)

from ResumeEnhancer.backend.app.schemas.unused.tailoring_decision import (
    TailoringDecision
)


def tailoring_decision_node(
    state: ResumeTailorState
):

    plan = state[
        "enhancement_plan"
    ]

    reasoning = state[
        "inventory_reasoning"
    ]

    decision = TailoringDecision(

        approved_skill_additions=
            plan.skills_to_add,

        approved_skill_emphasis=
            plan.skills_to_emphasize,

        summary_changes=
            plan.summary_improvements,

        experience_changes=
            plan.experience_improvements,

        keyword_targets=
            plan.keyword_targets
    )

    for skill in (
        reasoning.related_skills
    ):

        if (
            skill.skill
            not in decision.approved_skill_additions
        ):

            decision.approved_skill_additions.append(
                skill.skill
            )

    return {
        "tailoring_decision":
            decision
    }