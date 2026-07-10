
from typing import List, Optional

from pydantic import BaseModel, Field


# # ==========================================================
# # Contact Information
# # ==========================================================

# class ContactInfo(BaseModel):
#     location: Optional[str] = None
#     phone: Optional[str] = None
#     email: Optional[str] = None
#     linkedin: Optional[str] = None
#     github: Optional[str] = None
#     portfolio: Optional[str] = None


# # ==========================================================
# # Skills
# # ==========================================================

# class SkillCategory(BaseModel):
#     category: str
#     skills: List[str] = Field(default_factory=list)


# class SkillsSection(BaseModel):
#     categories: List[SkillCategory] = Field(default_factory=list)


# # ==========================================================
# # Professional Experience
# # ==========================================================

# class ProjectContribution(BaseModel):
#     title: str
#     bullet_points: List[str] = Field(default_factory=list)


# class ExperienceEntry(BaseModel):
#     company: str

#     role: str

#     location: Optional[str] = None

#     start_date: Optional[str] = None

#     end_date: Optional[str] = None

#     is_current: bool = False

#     responsibilities: List[str] = Field(
#         default_factory=list
#     )

#     projects: List[ProjectContribution] = Field(
#         default_factory=list
#     )


# # ==========================================================
# # Education
# # ==========================================================

# class EducationEntry(BaseModel):
#     degree: str

#     institution: str

#     field_of_study: Optional[str] = None

#     start_year: Optional[str] = None

#     end_year: Optional[str] = None

#     grade: Optional[str] = None


# # ==========================================================
# # Certification
# # ==========================================================

# class Certification(BaseModel):
#     name: str

#     issuer: Optional[str] = None

#     issue_date: Optional[str] = None

#     expiry_date: Optional[str] = None


# # ==========================================================
# # Projects
# # ==========================================================

# class ResumeProject(BaseModel):
#     name: str

#     description: Optional[str] = None

#     technologies: List[str] = Field(
#         default_factory=list
#     )

#     bullet_points: List[str] = Field(
#         default_factory=list
#     )


# # ==========================================================
# # Layout Information
# # ==========================================================

# class LayoutHints(BaseModel):

#     section_order: List[str] = Field(
#         default_factory=list
#     )

#     is_two_column: bool = False

#     primary_heading_size: int = 18

#     secondary_heading_size: int = 14

#     section_heading_size: int = 12

#     body_font_size: int = 10


# # ==========================================================
# # Resume Root
# # ==========================================================

# class ResumeDocument(BaseModel):

#     name: str

#     headline: str

#     contact_info: ContactInfo

#     professional_summary: str

#     technical_skills: SkillsSection

#     professional_experience: List[
#         ExperienceEntry
#     ] = Field(default_factory=list)

#     projects: List[
#         ResumeProject
#     ] = Field(default_factory=list)

#     certifications: List[
#         Certification
#     ] = Field(default_factory=list)

#     education: List[
#         EducationEntry
#     ] = Field(default_factory=list)

#     layout_hints: LayoutHints

# class ResumeDocument(BaseModel):

#     name: str

#     headline: str

#     contact_info: ContactInfo

#     professional_summary: str

#     technical_skills: SkillsSection

#     professional_experience: List[ExperienceEntry]

#     certifications: List[Certification]

#     education: List[EducationEntry]

#     layout_hints: LayoutHints


# class ContactInfo(BaseModel):
#     location: Optional[str] = None
#     phone: Optional[str] = None
#     email: Optional[str] = None
#     github: Optional[str] = None
#     linkedin: Optional[str] = None


# class SkillsSection(BaseModel):
#     languages: List[str] = []
#     frontend: List[str] = []
#     backend: List[str] = []
#     cloud_devops: List[str] = []
#     testing: List[str] = []
#     ai_genai: List[str] = []


# class ExperienceEntry(BaseModel):
#     company: str
#     role: str

#     start_date: Optional[str] = None
#     end_date: Optional[str] = None

#     location: Optional[str] = None

#     responsibilities: List[str] = []


# class Certification(BaseModel):
#     name: str


# class EducationEntry(BaseModel):
#     degree: str

#     institution: str

#     start_year: Optional[str] = None

#     end_year: Optional[str] = None


# class LayoutHints(BaseModel):

#     primary_heading_size: int

#     secondary_heading_size: int

#     section_heading_size: int

#     body_font_size: int

#     is_two_column: bool

#     section_order: list[str]


# from pydantic import BaseModel, Field, model_validator
# from typing import List, Optional

# class ContactInfo(BaseModel):
#     location: Optional[str] = None
#     phone: Optional[str] = None
#     email: Optional[str] = None
#     github: Optional[str] = None
#     linkedin: Optional[str] = None

# class SkillsSection(BaseModel):
#     languages: List[str] = Field(default_factory=list)
#     frontend: List[str] = Field(default_factory=list)
#     backend: List[str] = Field(default_factory=list)
#     cloud_devops: List[str] = Field(default_factory=list)
#     testing: List[str] = Field(default_factory=list)
#     ai_genai: List[str] = Field(default_factory=list)

# class ExperienceEntry(BaseModel):
#     company: str = "Unknown Company"
#     role: str = "Software Engineer"
#     start_date: Optional[str] = None
#     end_date: Optional[str] = None
#     location: Optional[str] = None
#     responsibilities: List[str] = Field(default_factory=list)

# class Certification(BaseModel):
#     name: str

#     @model_validator(mode="before")
#     @classmethod
#     def coerce_string_to_dict(cls, data):
#         """Converts raw string certificates like "AWS Certified" -> {"name": "AWS Certified"}"""
#         if isinstance(data, str):
#             return {"name": data}
#         return data

# class EducationEntry(BaseModel):
#     degree: str = "Degree"
#     institution: str = "Institution"
#     start_year: Optional[str] = None
#     end_year: Optional[str] = None

# class LayoutHints(BaseModel):
#     primary_heading_size: int = 18
#     secondary_heading_size: int = 14
#     section_heading_size: int = 12
#     body_font_size: int = 10
#     is_two_column: bool = False
#     section_order: List[str] = Field(default_factory=list)

# class ResumeDocument(BaseModel):
#     name: str = ""
#     headline: str = ""
#     professional_summary: str = ""

#     # Nested configurations utilizing default instantiation if omitted entirely
#     contact_info: ContactInfo = Field(default_factory=ContactInfo)
#     technical_skills: SkillsSection = Field(default_factory=SkillsSection)
#     layout_hints: LayoutHints = Field(default_factory=LayoutHints)

#     # Lists instantiated with empty factories safely
#     professional_experience: List[ExperienceEntry] = Field(
#         default_factory=list)
#     certifications: List[Certification] = Field(default_factory=list)
#     education: List[EducationEntry] = Field(default_factory=list)

#     @model_validator(mode="before")
#     @classmethod
#     def normalize_arrays(cls, data):
#         """Pre-processing validation step managing structural variations from LLMs"""
#         if not isinstance(data, dict):
#             return data

#         # Fix: education dict -> list conversion natively inside the model configuration
#         if "education" in data and isinstance(data["education"], dict):
#             data["education"] = [data["education"]]

#         return data
