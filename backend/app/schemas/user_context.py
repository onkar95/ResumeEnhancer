from pydantic import BaseModel, Field
from typing import List, Optional


class DeclaredSkill(BaseModel):
    """A skill/technology the candidate explicitly mentioned in free text,
    not necessarily present on the resume or in the inventory yet."""

    skill: str

    confidence: float = 0.6

    note: Optional[str] = None


class UserContext(BaseModel):
    """Structured version of the optional free-form instructions box."""

    raw_instructions: str = ""

    declared_skills: List[DeclaredSkill] = Field(default_factory=list)

    # "aggressive" | "strict" | "balanced" | None
    tailoring_mode: Optional[str] = None