# from app.workflows.state import (
#     ResumeTailorState
# )

# from app.schemas.validation_result import (
#     ValidationResult
# )


# def extract_resume_skills(
#     resume
# ):

#     skills = set()

#     for category in (
#         resume.technical_skills.categories
#     ):

#         for skill in category.skills:

#             skills.add(
#                 skill.lower()
#             )

#     return skills


# def validation_node(
#     state: ResumeTailorState
# ):

#     tailored_resume = (
#         state[
#             "tailored_resume"
#         ]
#     )

#     gap_analysis = (
#         state[
#             "gap_analysis"
#         ]
#     )

#     skills = extract_resume_skills(
#         tailored_resume
#     )

#     missing_keywords = []

#     for keyword in (
#         gap_analysis.missing_keywords
#     ):

#         if (
#             keyword.lower()
#             not in skills
#         ):

#             missing_keywords.append(
#                 keyword
#             )

#     coverage = 100

#     if gap_analysis.missing_keywords:

#         coverage = int(
#             (
#                 len(
#                     gap_analysis
#                     .matched_keywords
#                 )
#                 /
#                 (
#                     len(
#                         gap_analysis
#                         .matched_keywords
#                     )
#                     +
#                     len(
#                         gap_analysis
#                         .missing_keywords
#                     )
#                 )
#             )
#             * 100
#         )

#     result = ValidationResult(

#         is_valid=
#             len(
#                 missing_keywords
#             ) < 10,

#         missing_required_keywords=
#             missing_keywords,

#         keyword_coverage=
#             coverage
#     )

#     return {
#         "validation_result":
#             result
#     }
from app.workflows.state import (
    ResumeTailorState
)

from app.schemas.validation_result import (
    ValidationResult
)


def resume_to_text(
    resume
):

    chunks = []

    if resume.headline:

        chunks.append(
            resume.headline
        )

    if (
        resume.professional_summary
        and
        resume.professional_summary.content
    ):

        chunks.append(
            resume.professional_summary.content
        )

    for category in (
        resume.technical_skills.categories
    ):

        chunks.extend(
            category.skills
        )

    for experience in (
        resume.professional_experience
    ):

        if experience.role:
            chunks.append(
                experience.role
            )

        if experience.company:
            chunks.append(
                experience.company
            )

        chunks.extend(
            experience.responsibilities
        )

        for project in (
            experience.projects
        ):

            if project.title:

                chunks.append(
                    project.title
                )

            chunks.extend(
                project.bullet_points
            )

    return " ".join(
        str(chunk)
        for chunk in chunks
        if chunk
    ).lower()


def validation_node(
    state: ResumeTailorState
):

    tailored_resume = (
        state[
            "tailored_resume"
        ]
    )

    gap_analysis = (
        state[
            "gap_analysis"
        ]
    )

    resume_text = (
        resume_to_text(
            tailored_resume
        )
    )

    missing_keywords = []

    matched_count = 0

    total_keywords = (
        len(
            gap_analysis.matched_keywords
        )
        +
        len(
            gap_analysis.missing_keywords
        )
    )

    all_keywords = (
        gap_analysis.matched_keywords
        +
        gap_analysis.missing_keywords
    )

    for keyword in all_keywords:

        if (
            keyword.lower()
            in resume_text
        ):

            matched_count += 1

        else:

            missing_keywords.append(
                keyword
            )

    coverage = 100

    if total_keywords:

        coverage = int(
            (
                matched_count
                / total_keywords
            )
            * 100
        )

    result = ValidationResult(

        is_valid=coverage >= 70,

        missing_required_keywords=missing_keywords,

        keyword_coverage=coverage
    )

    return {
        "validation_result":
            result
    }
