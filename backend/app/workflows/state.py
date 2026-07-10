from typing import Optional
from typing_extensions import TypedDict

from app.schemas.resume import ResumeDocument
from app.schemas.job_description import JobDescription

from app.schemas.resume_inventory import (
    ResumeInventory
)

from app.schemas.candidate_suggestion import (
    CandidateSuggestion
)

from app.schemas.gap_analysis import (
    GapAnalysis
)

from app.schemas.enhancement_plan import (
    EnhancementPlan
)

from app.schemas.inventory_reasoning import (
    InventoryReasoning
)

from app.schemas.tailoring_context import (
    TailoringContext
)

from app.schemas.tailoring_decision import (
    TailoringDecision
)

from app.schemas.validation_result import (
    ValidationResult
)

from app.schemas.comparison_result import (
    ComparisonResult
)


class ResumeTailorState(
    TypedDict
):

    resume_pdf_path: str

    jd_text: str

    parsed_resume: Optional[
        ResumeDocument
    ]

    parsed_jd: Optional[
        JobDescription
    ]

    resume_inventory: Optional[
        ResumeInventory
    ]

    candidate_suggestions: Optional[
        CandidateSuggestion
    ]

    approved_suggestions: Optional[
        CandidateSuggestion
    ]

    gap_analysis: Optional[
        GapAnalysis
    ]

    inventory_reasoning: Optional[
        InventoryReasoning
    ]

    enhancement_plan: Optional[
        EnhancementPlan
    ]

    tailoring_context: Optional[
        TailoringContext
    ]

    tailoring_decision: Optional[
        TailoringDecision
    ]

    tailored_resume: Optional[
        ResumeDocument
    ]

    validation_result: Optional[
        ValidationResult
    ]

    comparison_data: Optional[
        ComparisonResult
    ]

    retry_count: int

    error: Optional[str]


# from typing import Optional
# from typing_extensions import TypedDict

# from app.schemas.resume import ResumeDocument
# from app.schemas.job_description import JobDescription


# class ResumeTailorState(TypedDict):

#     resume_pdf_path: str
#     jd_text: str

#     parsed_resume: Optional[ResumeDocument]

#     parsed_jd: Optional[JobDescription]

#     gap_analysis: Optional[dict]

#     tailored_resume: Optional[ResumeDocument]

#     validation_result: Optional[dict]

#     comparison_data: Optional[dict]

#     retry_count: int

#     error: Optional[str]
