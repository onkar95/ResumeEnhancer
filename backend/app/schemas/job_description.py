from typing import List, Optional

from pydantic import BaseModel, Field


# ==========================================================
# JOB DETAILS
# ==========================================================

class JobDetails(BaseModel):

    title: Optional[str] = None

    company: Optional[str] = None

    location: Optional[str] = None

    employment_type: Optional[str] = None

    experience_required: Optional[str] = None


# ==========================================================
# JOB DESCRIPTION
# ==========================================================

class JobDescription(BaseModel):

    job_details: JobDetails

    summary: Optional[str] = None

    responsibilities: List[str] = Field(
        default_factory=list
    )

    required_skills: List[str] = Field(
        default_factory=list
    )

    preferred_skills: List[str] = Field(
        default_factory=list
    )

    qualifications: List[str] = Field(
        default_factory=list
    )

    keywords: List[str] = Field(
        default_factory=list
    )

    education_required: Optional[str] = None