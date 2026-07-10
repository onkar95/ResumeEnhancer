from app.workflows.state import (
    ResumeTailorState
)

from app.schemas.validation_result import (
    ValidationResult
)


def extract_resume_skills(
    resume
):

    skills = set()

    for category in (
        resume.technical_skills.categories
    ):

        for skill in category.skills:

            skills.add(
                skill.lower()
            )

    return skills


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

    skills = extract_resume_skills(
        tailored_resume
    )

    missing_keywords = []

    for keyword in (
        gap_analysis.missing_keywords
    ):

        if (
            keyword.lower()
            not in skills
        ):

            missing_keywords.append(
                keyword
            )

    coverage = 100

    if gap_analysis.missing_keywords:

        coverage = int(
            (
                len(
                    gap_analysis
                    .matched_keywords
                )
                /
                (
                    len(
                        gap_analysis
                        .matched_keywords
                    )
                    +
                    len(
                        gap_analysis
                        .missing_keywords
                    )
                )
            )
            * 100
        )

    result = ValidationResult(

        is_valid=
            len(
                missing_keywords
            ) < 10,

        missing_required_keywords=
            missing_keywords,

        keyword_coverage=
            coverage
    )

    return {
        "validation_result":
            result
    }