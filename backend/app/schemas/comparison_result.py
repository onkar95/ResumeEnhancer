from pydantic import BaseModel, Field
from typing import List


class ComparisonResult(BaseModel):

    inventory_skills_used: List[str] = Field(
        default_factory=list
    )

    approved_skills_added: List[str] = Field(
        default_factory=list
    )

    emphasized_skills: List[str] = Field(
        default_factory=list
    )

    targeted_keywords: List[str] = Field(
        default_factory=list
    )

    summary_updated: bool = False

    experience_sections_updated: int = 0

    ats_before: int = 0

    ats_after: int = 0