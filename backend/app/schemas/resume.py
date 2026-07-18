"""
ResumeDocument Schema

Standardized resume used by the application for:

- Resume Tailoring
- Resume Generation
- HTML Rendering
- PDF Generation

This is NOT the parser schema.

Pipeline:

RawResumeDocument
        ↓
CanonicalResume
        ↓
ResumeDocument
"""

from typing import List, Optional

from pydantic import BaseModel, Field


# ==========================================================
# CONTACT INFORMATION
# ==========================================================

class ContactInfo(BaseModel):
    """Candidate contact information."""

    location: Optional[str] = None

    phone: Optional[str] = None

    email: Optional[str] = None

    github: Optional[str] = None

    linkedin: Optional[str] = None

    portfolio: Optional[str] = None


# ==========================================================
# PROFESSIONAL SUMMARY
# ==========================================================

class ProfessionalSummary(BaseModel):
    """Professional summary."""

    content: str


# ==========================================================
# TECHNICAL SKILLS
# ==========================================================

class SkillCategory(BaseModel):
    """
    Dynamic skill category.

    Examples

    Languages

    Frontend

    Backend

    Cloud

    AI

    Databases

    DevOps

    Frameworks

    Libraries
    """

    category: str

    skills: List[str] = Field(default_factory=list)


class SkillsSection(BaseModel):
    """
    Technical Skills.

    Categories are intentionally dynamic.

    Example

    [
        {
            "category": "Languages",
            "skills": [
                "JavaScript",
                "Python"
            ]
        },
        {
            "category": "Frontend",
            "skills": [
                "React",
                "Next.js"
            ]
        }
    ]
    """

    categories: List[SkillCategory] = Field(default_factory=list)


# ==========================================================
# EXPERIENCE PROJECT
# ==========================================================

class ExperienceProject(BaseModel):
    """
    Represents one project/contribution under a company.
    """

    title: str

    bullet_points: List[str] = Field(default_factory=list)
    
    technologies: List[str] = Field(
        default_factory=list,
        description=(
            "Tech stack explicitly listed for this project on the resume "
            "(e.g. a subtitle line like 'React Native, Node.js, Express, "
            "MongoDB' under a project title). Used for JD relevance "
            "matching -- do NOT infer these; only capture what the resume "
            "explicitly states."
        )
    )


# ==========================================================
# PROFESSIONAL EXPERIENCE
# ==========================================================

class ExperienceEntry(BaseModel):
    """
    One company experience.
    """

    company: str

    role: str

    location: Optional[str] = None

    start_date: Optional[str] = None

    end_date: Optional[str] = None

    responsibilities: List[str] = Field(default_factory=list)

    projects: List[ExperienceProject] = Field(default_factory=list)


# ==========================================================
# CERTIFICATIONS
# ==========================================================

class Certification(BaseModel):
    name: str


# ==========================================================
# EDUCATION
# ==========================================================

class EducationEntry(BaseModel):
    degree: str

    institution: str

    start_year: Optional[str] = None

    end_year: Optional[str] = None


# ==========================================================
# LAYOUT
# ==========================================================

class LayoutHints(BaseModel):
    """
    Logical layout only.

    Actual styling belongs to the PDF renderer.
    """

    is_two_column: bool = False

    section_order: List[str] = Field(
        default_factory=lambda: [
            "professional_summary",
            "technical_skills",
            "professional_experience",
            "certifications",
            "education",
        ]
    )


# ==========================================================
# ROOT DOCUMENT
# ==========================================================

class ResumeDocument(BaseModel):
    """
    Final standardized resume.

    Used by:

    - Resume Tailoring
    - HTML Generation
    - PDF Generation
    """

    name: str

    headline: str

    contact_info: ContactInfo

    professional_summary: ProfessionalSummary

    technical_skills: SkillsSection

    professional_experience: List[ExperienceEntry] = Field(
        default_factory=list)

    certifications: List[Certification] = Field(default_factory=list)

    education: List[EducationEntry] = Field(default_factory=list)

    layout_hints: LayoutHints = Field(default_factory=LayoutHints)
