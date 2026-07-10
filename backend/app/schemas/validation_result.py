from pydantic import BaseModel, Field
from typing import List


class ValidationResult(BaseModel):

    is_valid: bool = True

    invented_content: List[str] = Field(
        default_factory=list
    )

    missing_required_keywords: List[str] = Field(
        default_factory=list
    )

    keyword_coverage: int = 0

    warnings: List[str] = Field(
        default_factory=list
    )

