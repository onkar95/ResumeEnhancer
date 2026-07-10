from app.workflows.state import (
    ResumeTailorState
)

from app.schemas.enhancement_plan import (
    EnhancementPlan
)


def enhancement_plan_node(
    state: ResumeTailorState
):

    gap_analysis = state[
        "gap_analysis"
    ]

    plan = EnhancementPlan()

    # safe additions
    plan.skills_to_add.extend(
        gap_analysis.available_in_inventory
    )

    # emphasize existing skills
    plan.skills_to_emphasize.extend(
        gap_analysis.already_present
    )

    # target keywords
    plan.keyword_targets.extend(
        gap_analysis.missing_keywords
    )

    # summary suggestions

    if (
        gap_analysis.available_in_inventory
    ):

        plan.summary_improvements.append(
            "Include inventory skills relevant to the JD in the professional summary."
        )

    if (
        gap_analysis.already_present
    ):

        plan.summary_improvements.append(
            "Highlight strongest matching skills from the current resume."
        )

    # experience improvements

    for skill in (
        gap_analysis.available_in_inventory
    ):

        plan.experience_improvements.append(
            f"Add evidence demonstrating experience with {skill} where appropriate."
        )

    return {
        "enhancement_plan":
            plan
    }