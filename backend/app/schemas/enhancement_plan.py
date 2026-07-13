from pydantic import BaseModel, Field
from typing import List


class EnhancementPlan(BaseModel):

    skills_to_add: List[str] = Field(
        default_factory=list
    )

    skills_to_emphasize: List[str] = Field(
        default_factory=list
    )

    summary_improvements: List[str] = Field(
        default_factory=list
    )

    experience_improvements: List[str] = Field(
        default_factory=list
    )

    keyword_targets: List[str] = Field(
        default_factory=list
    )

# from app.workflows.state import ResumeTailorState

# from app.schemas.enhancement_plan import (
#     EnhancementPlan
# )


# def enhancement_plan_node(
#     state: ResumeTailorState
# ):

#     gap_analysis = state["gap_analysis"]

#     plan = EnhancementPlan()

#     plan.skills_to_add = list(
#         gap_analysis.available_in_inventory
#     )

#     plan.skills_to_emphasize = list(
#         gap_analysis.already_present
#     )

#     plan.keyword_targets = list(
#         gap_analysis.missing_keywords
#     )

#     if plan.skills_to_add:

#         plan.summary_improvements.append(
#             "Include inventory skills relevant to the target role."
#         )

#     if plan.skills_to_emphasize:

#         plan.summary_improvements.append(
#             "Highlight strongest matching skills already present in the resume."
#         )

#     for skill in plan.skills_to_add:

#         plan.experience_improvements.append(
#             f"Add evidence of experience with {skill} where truthful and supported."
#         )

#     return {
#         "enhancement_plan": plan
#     }