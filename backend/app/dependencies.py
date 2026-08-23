"""
Application Dependencies

Provides singleton service instances.
"""

from functools import lru_cache

from app.services.groq_service import (
    GroqService,
)

from app.services.pdf_extraction_service import (
    PDFExtractionService,
)

from app.services.resume_parser_service import (
    ResumeParserService,
)
from fastapi import Request, HTTPException

from app.core.security import decode_access_token
from app.services.user_service import get_user_by_id


@lru_cache
def get_pdf_service() -> PDFExtractionService:
    return PDFExtractionService()


@lru_cache
def get_groq_service() -> GroqService:
    return GroqService()


@lru_cache
def get_resume_parser() -> ResumeParserService:
    return ResumeParserService()



def get_current_user(request: Request) -> dict:
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    payload = decode_access_token(token)

    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    user = get_user_by_id(payload["sub"])

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user