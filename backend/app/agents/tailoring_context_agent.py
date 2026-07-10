from app.workflows.state import (
    ResumeTailorState
)

from app.schemas.tailoring_context import (
    TailoringContext
)


def tailoring_context_node(
    state: ResumeTailorState
):

    resume = state[
        "parsed_resume"
    ]

    inventory = state[
        "resume_inventory"
    ]

    plan = state[
        "enhancement_plan"
    ]

    reasoning = state[
        "inventory_reasoning"
    ]

    resume_skills = []

    for category in (
        resume.technical_skills.categories
    ):

        resume_skills.extend(
            category.skills
        )

    inventory_skills = [
        skill.name
        for skill in inventory.skills
    ]

    inferred_skills = [

        item.skill

        for item in (
            reasoning.related_skills
        )
    ]

    context = TailoringContext(

        current_resume_skills=
            resume_skills,

        inventory_skills=
            inventory_skills,

        approved_skills=[],

        skills_to_add=
            plan.skills_to_add,

        skills_to_emphasize=
            plan.skills_to_emphasize,

        keyword_targets=
            plan.keyword_targets,

        inferred_skills=
            inferred_skills,

        inferred_experience=
            reasoning.inferred_experience
    )

    return {
        "tailoring_context":
            context
    }