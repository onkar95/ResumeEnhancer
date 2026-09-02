from pydantic import BaseModel

from app.schemas.resume import (
    ResumeDocument
)

from app.schemas.validation_result import (
    ValidationResult
)

from app.schemas.comparison_result import (
    ComparisonResult
)


class WorkflowResult(
    BaseModel
):

    tailored_resume: ResumeDocument

    validation: ValidationResult

    comparison: ComparisonResult
