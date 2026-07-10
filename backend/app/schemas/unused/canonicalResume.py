"""
Canonical Resume Schema

This is the application's internal resume representation.

Every resume source eventually becomes a CanonicalResume.

Sources

- PDF
- DOCX
- LinkedIn
- GitHub
- Portfolio Website
- JSON Resume

All AI modules consume this model.

Author: Resume Tailor AI
"""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


# ==========================================================
# PERSONAL INFORMATION
# ==========================================================


class PersonalInformation(BaseModel):

    full_name: str

    headline: str

    location: Optional[str] = None

    phone: Optional[str] = None

    email: Optional[str] = None

    linkedin: Optional[str] = None

    github: Optional[str] = None

    portfolio: Optional[str] = None

    website: Optional[str] = None


# ==========================================================
# SUMMARY
# ==========================================================


class Summary(BaseModel):

    content: str


# ==========================================================
# SKILLS
# ==========================================================


class Skill(BaseModel):

    name: str

    category: Optional[str] = None

    years_of_experience: Optional[float] = None

    proficiency: Optional[str] = None


# ==========================================================
# EXPERIENCE
# ==========================================================


class Experience(BaseModel):

    company: str

    role: str

    location: Optional[str] = None

    start_date: Optional[str] = None

    end_date: Optional[str] = None

    is_current: bool = False

    responsibilities: List[str] = Field(
        default_factory=list
    )

    technologies: List[str] = Field(
        default_factory=list
    )


# ==========================================================
# PROJECT
# ==========================================================


class Project(BaseModel):

    name: str

    description: Optional[str] = None

    technologies: List[str] = Field(
        default_factory=list
    )

    bullet_points: List[str] = Field(
        default_factory=list
    )

    github: Optional[str] = None

    live_demo: Optional[str] = None


# ==========================================================
# EDUCATION
# ==========================================================


class Education(BaseModel):

    degree: str

    institution: str

    field_of_study: Optional[str] = None

    start_year: Optional[str] = None

    end_year: Optional[str] = None

    grade: Optional[str] = None


# ==========================================================
# CERTIFICATION
# ==========================================================


class Certification(BaseModel):

    name: str

    issuer: Optional[str] = None

    issue_date: Optional[str] = None

    expiry_date: Optional[str] = None


# ==========================================================
# ACHIEVEMENT
# ==========================================================


class Achievement(BaseModel):

    title: str

    description: Optional[str] = None


# ==========================================================
# LANGUAGE
# ==========================================================


class Language(BaseModel):

    name: str

    proficiency: Optional[str] = None


# ==========================================================
# CUSTOM SECTION
# ==========================================================


class CustomSection(BaseModel):
    """
    Stores sections we don't understand yet.

    Example

    Publications

    Patents

    Awards

    Interests

    Hobbies

    Volunteer Work

    etc.
    """

    title: str

    items: List[str] = Field(
        default_factory=list
    )


# ==========================================================
# METADATA
# ==========================================================


class ResumeMetadata(BaseModel):

    source: str = "pdf"

    parser_version: str = "1.0"

    confidence_score: float = 1.0

    detected_sections: List[str] = Field(
        default_factory=list
    )

    warnings: List[str] = Field(
        default_factory=list
    )


# ==========================================================
# ROOT
# ==========================================================


class CanonicalResume(BaseModel):

    personal_information: PersonalInformation

    summary: Summary

    skills: List[Skill] = Field(
        default_factory=list
    )

    experience: List[Experience] = Field(
        default_factory=list
    )

    projects: List[Project] = Field(
        default_factory=list
    )

    education: List[Education] = Field(
        default_factory=list
    )

    certifications: List[Certification] = Field(
        default_factory=list
    )

    achievements: List[Achievement] = Field(
        default_factory=list
    )

    languages: List[Language] = Field(
        default_factory=list
    )

    custom_sections: List[
        CustomSection
    ] = Field(default_factory=list)

    metadata: ResumeMetadata = Field(
        default_factory=ResumeMetadata
    )