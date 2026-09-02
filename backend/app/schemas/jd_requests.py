
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
    

