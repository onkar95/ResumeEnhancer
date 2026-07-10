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