"""
Raw Resume Schema

This schema represents the uploaded resume as faithfully as possible.

Unlike ResumeDocument, this model DOES NOT normalize section names.

Examples

Resume A
--------
TECHNICAL SKILLS
Frontend
Backend

Resume B
--------
CORE COMPETENCIES
Programming Languages
Frameworks

Both are preserved exactly.

This becomes the input for CanonicalResumeBuilder.

Author: Resume Tailor AI
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ==========================================================
# RAW CONTACT INFORMATION
# ==========================================================


class RawContactInfo(BaseModel):
    """
    Contact information extracted directly from resume.
    """

    location: Optional[str] = None

    phone: Optional[str] = None

    email: Optional[str] = None

    linkedin: Optional[str] = None

    github: Optional[str] = None

    portfolio: Optional[str] = None

    website: Optional[str] = None

    others: Dict[str, str] = Field(default_factory=dict)


# ==========================================================
# RAW SECTION ITEM
# ==========================================================


class RawSectionItem(BaseModel):
    """
    Represents a single piece of content.

    Could be

    - Bullet point
    - Paragraph
    - Key-value pair
    """

    text: str

    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )


# ==========================================================
# RAW SUBSECTION
# ==========================================================


class RawSubSection(BaseModel):
    """
    Examples

    Languages

    Frameworks

    Backend

    Cloud

    etc.
    """

    title: str

    items: List[
        RawSectionItem
    ] = Field(default_factory=list)

    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )


# ==========================================================
# RAW SECTION
# ==========================================================


class RawSection(BaseModel):
    """
    Top-level section.

    Examples

    EXPERIENCE

    SKILLS

    PROJECTS

    EDUCATION

    CERTIFICATIONS

    ACHIEVEMENTS

    PUBLICATIONS

    etc.
    """

    title: str

    order: int

    content: List[
        RawSectionItem
    ] = Field(default_factory=list)

    subsections: List[
        RawSubSection
    ] = Field(default_factory=list)

    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )


# ==========================================================
# RAW HEADER
# ==========================================================


class RawHeader(BaseModel):
    """
    Resume header.

    Everything above the first section.
    """

    name: Optional[str] = None

    headline: Optional[str] = None

    contact_info: RawContactInfo = Field(
        default_factory=RawContactInfo
    )

    extra_lines: List[str] = Field(
        default_factory=list
    )


# ==========================================================
# RAW DOCUMENT METADATA
# ==========================================================


class RawDocumentMetadata(BaseModel):
    """
    Metadata about the uploaded document.
    """

    filename: Optional[str] = None

    page_count: int = 0

    detected_layout: Optional[str] = None

    language: Optional[str] = None

    parser_version: str = "1.0"


# ==========================================================
# ROOT DOCUMENT
# ==========================================================


class RawResumeDocument(BaseModel):
    """
    Exact representation of uploaded resume.

    Nothing here is normalized.

    Sections retain their original names.

    Ordering is preserved.

    Sub-headings are preserved.

    Bullet points are preserved.

    This object is later transformed into

    CanonicalResume
    """

    header: RawHeader = Field(
        default_factory=RawHeader
    )

    sections: List[
        RawSection
    ] = Field(default_factory=list)

    metadata: RawDocumentMetadata = Field(
        default_factory=RawDocumentMetadata
    )