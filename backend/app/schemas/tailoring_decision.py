from pydantic import BaseModel, Field
from typing import List


class TailoringDecision(BaseModel):

    approved_skill_additions: List[str] = Field(
        default_factory=list
    )

    approved_skill_emphasis: List[str] = Field(
        default_factory=list
    )

    summary_changes: List[str] = Field(
        default_factory=list
    )

    experience_changes: List[str] = Field(
        default_factory=list
    )

    project_changes: List[str] = Field(
        default_factory=list
    )

    keyword_targets: List[str] = Field(
        default_factory=list
    )