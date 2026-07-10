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


@lru_cache
def get_pdf_service() -> PDFExtractionService:
    return PDFExtractionService()


@lru_cache
def get_groq_service() -> GroqService:
    return GroqService()


@lru_cache
def get_resume_parser() -> ResumeParserService:
    return ResumeParserService()