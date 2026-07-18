from uuid import uuid4

from app.utils.skill_normalizer import normalize_skill
from app.workflows.state import (
    ResumeTailorState
)

from app.schemas.candidate_suggestion import (
    CandidateSuggestion,
    Suggestion
)


def candidate_suggestion_node(
    state: ResumeTailorState
):
    """
    Surfaces suggestions the tailor step did NOT (or could not) apply on
    its own, for human review:

    - Skills in the inventory that are JD-relevant but still missing from
      the resume (the tailor LLM is instructed not to invent, so genuine
      gaps against inventory should still be surfaced here rather than
      silently dropped).
    - Certifications in inventory not on the resume.
    - Projects in inventory not on the resume.
    - Summary content in inventory not reflected in the current summary.

    Runs against the TAILORED resume (falling back to the original parsed
    resume if tailoring hasn't happened yet), since suggestions should
    describe what's still missing after the AI has already done its pass
    -- not restate things it already fixed.
    """

    resume = state.get("tailored_resume") or state["parsed_resume"]
    inventory = state["resume_inventory"]
    jd = state["parsed_jd"]

    suggestions = []

    # --------------------------------------------------
    # Skills Suggestions
    # --------------------------------------------------

    inventory_skills = {
        normalize_skill(skill.name)
        for skill in inventory.skills
    }

    resume_skills = {
        normalize_skill(skill)
        for category in resume.technical_skills.categories
        for skill in category.skills
    }

    jd_skills = (
        jd.required_skills
        + jd.preferred_skills
        + jd.keywords
    )

    for skill in set(jd_skills):

        normalized = normalize_skill(skill)

        if (
            normalized in inventory_skills
            and normalized not in resume_skills
        ):
            suggestions.append(
                Suggestion(
                    suggestion_id=str(uuid4()),
                    section="technical_skills",
                    subsection=None,
                    current_content=None,
                    suggested_content=skill,
                    reason=(
                        "Found in inventory and relevant "
                        "to JD but missing from resume."
                    ),
                    confidence=0.85
                )
            )

    # --------------------------------------------------
    # Certification Suggestions
    # --------------------------------------------------

    resume_certifications = {
        cert.name.lower()
        for cert in resume.certifications
    }

    for cert in inventory.certifications:

        if (
            cert.name.lower()
            not in resume_certifications
        ):

            suggestions.append(
                Suggestion(
                    suggestion_id=str(uuid4()),
                    section="certifications",
                    subsection=None,
                    current_content=None,
                    suggested_content=cert.name,
                    reason=(
                        "Certification exists in inventory "
                        "but is not included in resume."
                    ),
                    confidence=0.80
                )
            )

    # --------------------------------------------------
    # Project Suggestions
    # --------------------------------------------------

    resume_project_titles = {
        project.title.lower()
        for exp in resume.professional_experience
        for project in exp.projects
    }

    for exp in inventory.professional_experience:

        for project in exp.projects:

            if (
                project.title.lower()
                not in resume_project_titles
            ):

                suggestions.append(
                    Suggestion(
                        suggestion_id=str(uuid4()),
                        section="professional_experience",
                        subsection=exp.company,
                        current_content=None,
                        suggested_content={
                            "title": project.title,
                            "bullet_points": (
                                project.bullet_points
                            )
                        },
                        reason=(
                            f"Project from "
                            f"{exp.company} "
                            f"is missing from resume."
                        ),
                        confidence=0.90
                    )
                )

    # --------------------------------------------------
    # Summary Suggestions
    # --------------------------------------------------

    for summary in inventory.summary_points:

        if (
            summary.lower()
            not in resume.professional_summary
            .content.lower()
        ):

            suggestions.append(
                Suggestion(
                    suggestion_id=str(uuid4()),
                    section="professional_summary",
                    subsection=None,
                    current_content=(
                        resume.professional_summary
                        .content
                    ),
                    suggested_content=summary,
                    reason=(
                        "Relevant summary content "
                        "exists in inventory."
                    ),
                    confidence=0.70
                )
            )

    return {
        "candidate_suggestions":
            CandidateSuggestion(
                suggestions=suggestions
            )
    }

# from uuid import uuid4

# from app.utils.skill_normalizer import normalize_skill
# from app.workflows.state import (
#     ResumeTailorState
# )

# from app.schemas.candidate_suggestion import (
#     CandidateSuggestion,
#     Suggestion
# )


# def candidate_suggestion_node(
#     state: ResumeTailorState
# ):

#     resume = state["parsed_resume"]
#     inventory = state["resume_inventory"]
#     jd = state["parsed_jd"]

#     suggestions = []

#     # --------------------------------------------------
#     # Skills Suggestions
#     # --------------------------------------------------

#     inventory_skills = {
#         normalize_skill(skill.name)
#         for skill in inventory.skills
#     }

#     resume_skills = {
#         normalize_skill(skill)
#         for category in resume.technical_skills.categories
#         for skill in category.skills
#     }

#     jd_skills = (
#         jd.required_skills
#         + jd.preferred_skills
#         + jd.keywords
#     )

#     for skill in set(jd_skills):

#         normalized = normalize_skill(skill)

#         if (
#             normalized in inventory_skills
#             and normalized not in resume_skills
#         ):
#             suggestions.append(
#                 Suggestion(
#                     suggestion_id=str(uuid4()),
#                     section="technical_skills",
#                     subsection=None,
#                     current_content=None,
#                     suggested_content=skill,
#                     reason=(
#                         "Found in inventory and relevant "
#                         "to JD but missing from resume."
#                     ),
#                     confidence=0.85
#                 )
#             )

#     # --------------------------------------------------
#     # Certification Suggestions
#     # --------------------------------------------------

#     resume_certifications = {
#         cert.name.lower()
#         for cert in resume.certifications
#     }

#     for cert in inventory.certifications:

#         if (
#             cert.name.lower()
#             not in resume_certifications
#         ):

#             suggestions.append(
#                 Suggestion(
#                     suggestion_id=str(uuid4()),
#                     section="certifications",
#                     subsection=None,
#                     current_content=None,
#                     suggested_content=cert.name,
#                     reason=(
#                         "Certification exists in inventory "
#                         "but is not included in resume."
#                     ),
#                     confidence=0.80
#                 )
#             )

#     # --------------------------------------------------
#     # Project Suggestions
#     # --------------------------------------------------

#     resume_project_titles = {
#         project.title.lower()
#         for exp in resume.professional_experience
#         for project in exp.projects
#     }

#     for exp in inventory.professional_experience:

#         for project in exp.projects:

#             if (
#                 project.title.lower()
#                 not in resume_project_titles
#             ):

#                 suggestions.append(
#                     Suggestion(
#                         suggestion_id=str(uuid4()),
#                         section="professional_experience",
#                         subsection=exp.company,
#                         current_content=None,
#                         suggested_content={
#                             "title": project.title,
#                             "bullet_points": (
#                                 project.bullet_points
#                             )
#                         },
#                         reason=(
#                             f"Project from "
#                             f"{exp.company} "
#                             f"is missing from resume."
#                         ),
#                         confidence=0.90
#                     )
#                 )

#     # --------------------------------------------------
#     # Summary Suggestions
#     # --------------------------------------------------

#     for summary in inventory.summary_points:

#         if (
#             summary.lower()
#             not in resume.professional_summary
#             .content.lower()
#         ):

#             suggestions.append(
#                 Suggestion(
#                     suggestion_id=str(uuid4()),
#                     section="professional_summary",
#                     subsection=None,
#                     current_content=(
#                         resume.professional_summary
#                         .content
#                     ),
#                     suggested_content=summary,
#                     reason=(
#                         "Relevant summary content "
#                         "exists in inventory."
#                     ),
#                     confidence=0.70
#                 )
#             )

#     return {
#         "candidate_suggestions":
#             CandidateSuggestion(
#                 suggestions=suggestions
#             )
#     }
