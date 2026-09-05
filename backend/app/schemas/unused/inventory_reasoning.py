from pydantic import BaseModel, Field
from typing import List


class RelatedSkill(BaseModel):

    skill: str

    reason: str

    confidence: float


class InventoryReasoning(BaseModel):

    related_skills: List[
        RelatedSkill
    ] = Field(default_factory=list)

    inferred_experience: List[
        str
    ] = Field(default_factory=list)

    inferred_keywords: List[
        str
    ] = Field(default_factory=list)