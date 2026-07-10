from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.resume import (
    ExperienceEntry,
    Certification,
    EducationEntry,
)


class InventorySkill(BaseModel):
    name: str

    rating: int = 0

    source: str = "resume"

    verified: bool = False


class ResumeVersion(BaseModel):

    filename: str

    uploaded_at: datetime


class ResumeInventory(BaseModel):

    professional_summaries: List[str] = Field(
        default_factory=list
    )

    skills: List[InventorySkill] = Field(
        default_factory=list
    )

    professional_experience: List[
        ExperienceEntry
    ] = Field(
        default_factory=list
    )

    certifications: List[
        Certification
    ] = Field(
        default_factory=list
    )

    education: List[
        EducationEntry
    ] = Field(
        default_factory=list
    )

    resume_versions: List[
        ResumeVersion
    ] = Field(
        default_factory=list
    )
    evidence: List[
        InventoryEvidence
    ] = Field(default_factory=list)

    updated_at: Optional[
        datetime
    ] = None


class InventoryEvidence(BaseModel):

    evidence_id: str

    title: str

    section: str

    content: str

    source: str

    created_at: datetime
