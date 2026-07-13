from pydantic import BaseModel, Field
from typing import List


class GapAnalysis(BaseModel):

    already_present: List[str] = Field(
        default_factory=list
    )

    available_in_inventory: List[str] = Field(
        default_factory=list
    )

    missing_and_unknown: List[str] = Field(
        default_factory=list
    )

    matched_keywords: List[str] = Field(
        default_factory=list
    )

    missing_keywords: List[str] = Field(
        default_factory=list
    )