from app.schemas.responses import APIResponse
from app.schemas.jd_requests import TailorResumeRequest
from app.schemas.resume import ResumeDocument
from app.schemas.job_description import JobDescription

# __all__ defines what gets exported when someone uses "from app.schemas import *"
# It also helps IDEs with auto-complete
__all__ = [
    "APIResponse",
    "TailorResumeRequest",
    "ResumeDocument",
    "JobDescription",
]