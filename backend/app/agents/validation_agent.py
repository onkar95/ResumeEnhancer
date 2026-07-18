from app.utils.text_matching import (
    resume_document_text,
    match_keywords,
)

from app.workflows.state import (
    ResumeTailorState
)

from app.schemas.validation_result import (
    ValidationResult
)


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

    resume_text = resume_document_text(
        tailored_resume
    )

    all_keywords = (
        gap_analysis.matched_keywords
        + gap_analysis.missing_keywords
    )

    matched_keywords, missing_keywords = match_keywords(
        all_keywords,
        resume_text
    )

    total_keywords = len(all_keywords)

    coverage = 100

    if total_keywords:

        coverage = int(
            (
                len(matched_keywords)
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