from pydantic import BaseModel, Field
from typing import List


class GapAnalysis(BaseModel):

    # already in current resume
    already_present: List[str] = Field(
        default_factory=list
    )

    # not in current resume but available in inventory
    available_in_inventory: List[str] = Field(
        default_factory=list
    )

    # neither in resume nor inventory
    missing_and_unknown: List[str] = Field(
        default_factory=list
    )

    matched_keywords: List[str] = Field(
        default_factory=list
    )

    missing_keywords: List[str] = Field(
        default_factory=list
    )

    ats_before: int = 0

    ats_after: int = 0