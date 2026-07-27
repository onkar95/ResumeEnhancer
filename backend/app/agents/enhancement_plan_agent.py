
from app.workflows.state import (
    ResumeTailorState
)

from app.schemas.enhancement_plan import (
    EnhancementPlan
)

from app.core.logger import (
    logger
)


def enhancement_plan_node(
    state: ResumeTailorState
):

    logger.info(
        "started enhancement_plan_agent"
    )

    gap_analysis = state[
        "gap_analysis"
    ]

    plan = EnhancementPlan()

    # --------------------------------------------------
    # Skills available in inventory but not currently
    # present in resume
    # --------------------------------------------------

    plan.skills_to_add.extend(
        sorted(
            set(
                gap_analysis.inventory_skills
            )
        )
    )

    # --------------------------------------------------
    # Skills already matching JD
    # --------------------------------------------------

    plan.skills_to_emphasize.extend(
        sorted(
            set(
                gap_analysis.matched_skills
            )
        )
    )

    # --------------------------------------------------
    # Relevant experience
    # --------------------------------------------------

    plan.experience_to_emphasize.extend(
        sorted(
            set(
                gap_analysis.relevant_experience
            )
        )
    )

    # --------------------------------------------------
    # Relevant projects
    # --------------------------------------------------

    plan.projects_to_emphasize.extend(
        sorted(
            set(
                gap_analysis.relevant_projects
            )
        )
    )

    # --------------------------------------------------
    # ATS Keywords
    # --------------------------------------------------

    plan.keyword_targets.extend(
        sorted(
            set(
                gap_analysis.missing_keywords
            )
        )
    )

    # --------------------------------------------------
    # Summary improvements
    #
    # IMPORTANT: this must cover BOTH matched skills (so
    # they get surfaced in the summary) AND missing JD
    # keyword phrases (so ATS text-search actually finds
    # them). Skills alone was the bug -- the tailor LLM
    # was never explicitly told to work phrases like
    # "deployment pipelines" or "operational excellence"
    # into the summary/bullets, so keyword_coverage stayed
    # at whatever the untouched original resume already had.
    # --------------------------------------------------

    for item in sorted(
        set(
            gap_analysis.summary_opportunities
        )
    ):

        plan.summary_improvements.append(
            f"Highlight {item} in the professional summary."
        )

    for keyword in sorted(
        set(
            gap_analysis.missing_keywords
        )
    ):

        plan.summary_improvements.append(
            f'Naturally work the JD phrase "{keyword}" into the '
            f"professional summary or an experience bullet, but ONLY "
            f"if it can be phrased truthfully based on the candidate's "
            f"actual experience -- do not force it in a way that "
            f"misrepresents their work."
        )

    logger.info(
        "enhancement_plan=%s",
        plan.model_dump()
    )

    return {
        "enhancement_plan": plan
    }

# from app.workflows.state import (
#     ResumeTailorState
# )

# from app.schemas.enhancement_plan import (
#     EnhancementPlan
# )

# from app.core.logger import (
#     logger
# )


# def enhancement_plan_node(
#     state: ResumeTailorState
# ):

#     logger.info(
#         "started enhancement_plan_agent"
#     )

#     gap_analysis = state[
#         "gap_analysis"
#     ]

#     plan = EnhancementPlan()

#     # --------------------------------------------------
#     # Skills available in inventory but not currently
#     # present in resume
#     # --------------------------------------------------

#     plan.skills_to_add.extend(
#         sorted(
#             set(
#                 gap_analysis.inventory_skills
#             )
#         )
#     )

#     # --------------------------------------------------
#     # Skills already matching JD
#     # --------------------------------------------------

#     plan.skills_to_emphasize.extend(
#         sorted(
#             set(
#                 gap_analysis.matched_skills
#             )
#         )
#     )

#     # --------------------------------------------------
#     # Relevant experience
#     # --------------------------------------------------

#     plan.experience_to_emphasize.extend(
#         sorted(
#             set(
#                 gap_analysis.relevant_experience
#             )
#         )
#     )

#     # --------------------------------------------------
#     # Relevant projects
#     # --------------------------------------------------

#     plan.projects_to_emphasize.extend(
#         sorted(
#             set(
#                 gap_analysis.relevant_projects
#             )
#         )
#     )

#     # --------------------------------------------------
#     # ATS Keywords
#     # --------------------------------------------------

#     plan.keyword_targets.extend(
#         sorted(
#             set(
#                 gap_analysis.missing_keywords
#             )
#         )
#     )

#     # --------------------------------------------------
#     # Summary improvements
#     # --------------------------------------------------

#     for item in sorted(
#         set(
#             gap_analysis.summary_opportunities
#         )
#     ):

#         plan.summary_improvements.append(
#             f"Highlight {item} in the professional summary."
#         )

#     logger.info(
#         "enhancement_plan=%s",
#         plan.model_dump()
#     )

#     return {
#         "enhancement_plan": plan
#     }
