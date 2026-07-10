
from pydantic import BaseModel, Field

from app.schemas.resume import ResumeDocument
from app.schemas.job_description import JobDescription


# ==========================================================
# PARSE JD REQUEST
# ==========================================================

class ParseJDRequest(BaseModel):
    """
    Raw JD text submitted by frontend.
    """

    job_description: str = Field(
        ...,
        min_length=10,
        description="Raw job description text"
    )


# ==========================================================
# PARSE JD RESPONSE
# ==========================================================

class ParseJDResponse(BaseModel):
    """
    Parsed structured JD.
    """

    success: bool = True

    data: JobDescription


# ==========================================================
# TAILOR REQUEST
# ==========================================================

class TailorResumeRequest(BaseModel):
    """
    M3 Tailoring request.

    Frontend flow:

    Resume PDF
        ↓
    ResumeDocument

    JD Text
        ↓
    JobDescription

    ResumeDocument + JobDescription
        ↓
    Tailored Resume
    """

    resume: ResumeDocument

    job_description: JobDescription


# ==========================================================
# TAILOR RESPONSE
# ==========================================================

class TailorResumeResponse(BaseModel):

    success: bool = True

    data: ResumeDocument
    

# from typing import Optional

# from pydantic import BaseModel, Field

# from app.schemas.job_description import JobDescription


# # ==========================================================
# # PARSE JD REQUEST
# # ==========================================================

# class ParseJDRequest(BaseModel):
#     """
#     Raw JD submitted by user.
#     """

#     job_description: str = Field(
#         ...,
#         min_length=10,
#         description="Raw job description text"
#     )


# # ==========================================================
# # PARSE JD RESPONSE
# # ==========================================================

# class ParseJDResponse(BaseModel):
#     """
#     Parsed JD response.
#     """

#     success: bool = True

#     message: str = "Job description parsed successfully"

#     data: JobDescription


# # ==========================================================
# # FUTURE TAILOR REQUEST
# # ==========================================================

# class TailorResumeRequest(BaseModel):
#     """
#     Future endpoint contract.

#     This schema is intentionally added now
#     so APIs remain stable when tailoring
#     is implemented.
#     """

#     resume_id: Optional[str] = None

#     job_description: str


# # ==========================================================
# # FUTURE ANALYSIS REQUEST
# # ==========================================================

# class AnalyzeJDRequest(BaseModel):
#     """
#     Future ATS analysis.
#     """

#     job_description: str


# # ==========================================================
# # FUTURE SKILL GAP RESPONSE
# # ==========================================================

# class SkillGapResponse(BaseModel):

#     matched_skills: list[str] = []

#     missing_skills: list[str] = []

#     match_percentage: float = 0.0


# # ==========================================================
# # FUTURE ATS RESPONSE
# # ==========================================================

# class ATSAnalysisResponse(BaseModel):

#     score: float = 0.0

#     strengths: list[str] = []

#     weaknesses: list[str] = []

#     recommendations: list[str] = []