"""
Resume API

Endpoints

POST /upload
    Upload resume and extract text.

POST /parse
    Upload resume and parse into ResumeDocument.

POST /tailor
    Tailor ResumeDocument against JobDescription.
"""
from pathlib import Path
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

# Centralized Imports
from app.core.constants import SUPPORTED_EXTENSIONS, UPLOAD_DIR
from app.dependencies import get_pdf_service, get_resume_parser
from app.schemas import APIResponse, TailorResumeRequest, ResumeDocument, JobDescription
from app.services import PDFExtractionService, ResumeParserService, ResumeTailorService


router = APIRouter(
    tags=["Resume"],
)


# ==========================================================
# Helpers
# ==========================================================


def validate_pdf(file: UploadFile) -> None:
    """
    Validate uploaded resume.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing.",
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )


async def save_upload_file(
    file: UploadFile,
) -> Path:
    """
    Save uploaded PDF locally.
    """

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        buffer.write(
            await file.read()
        )

    return file_path


# ==========================================================
# Upload Endpoint
# ==========================================================


@router.post(
    "/upload",
    response_model=APIResponse,
)
async def upload_resume(
    resume: UploadFile = File(...),
    pdf_service: PDFExtractionService = Depends(
        get_pdf_service
    ),
):
    """
    Upload resume and extract raw text.
    """

    validate_pdf(resume)

    file_path = await save_upload_file(
        resume
    )

    extracted_text = pdf_service.extract_text(
        str(file_path)
    )

    return APIResponse(
        success=True,
        message="Resume uploaded successfully.",
        data={
            "filename": resume.filename,
            "text": extracted_text,
        },
    )


# ==========================================================
# Parse Endpoint
# ==========================================================


@router.post(
    "/parse",
    response_model=APIResponse,
)
async def parse_resume(
    resume: UploadFile = File(...),
    pdf_service: PDFExtractionService = Depends(
        get_pdf_service
    ),
    parser: ResumeParserService = Depends(
        get_resume_parser
    ),
):
    """
    Upload resume, extract text,
    parse it using Groq and return
    ResumeDocument JSON.
    """

    validate_pdf(resume)

    file_path = await save_upload_file(
        resume
    )

    resume_text = pdf_service.extract_text(
        str(file_path)
    )

    parsed_resume = await parser.parse_resume(
        resume_text
    )

    return APIResponse(
        success=True,
        message="Resume parsed successfully.",
        data=parsed_resume.model_dump(),
    )


# ==========================================================
# Tailor Endpoint
# ==========================================================


@router.post(
    "/tailor",
    response_model=APIResponse,
)
async def tailor_resume(
    request: TailorResumeRequest,
):
    """
    Tailor ResumeDocument using
    parsed JobDescription.
    """

    tailor_service = ResumeTailorService()

    tailored_resume = await tailor_service.tailor(
        resume=request.resume,
        job_description=request.job_description,
    )

    return APIResponse(
        success=True,
        message="Resume tailored successfully.",
        data=tailored_resume.model_dump(),
    )
    
    
# from pathlib import Path

# from fastapi import APIRouter, UploadFile, File

# from app.services.pdf_extraction_service import PDFExtractionService
# from app.services.resume_parser_service import (
#     ResumeParserService
# )
# from app.utils.json_utils import (
#     parse_llm_json
# )
# from app.schemas.resume import (
#     ResumeDocument
# )
# from app.utils.resume_normalizer import (

#     normalize_resume
# )

# router = APIRouter()

# UPLOAD_DIR = Path("uploads")
# UPLOAD_DIR.mkdir(exist_ok=True)


# @router.post("/upload")
# async def upload_resume(
#     resume: UploadFile = File(...)
# ):
#     file_path = UPLOAD_DIR / resume.filename

#     with open(file_path, "wb") as buffer:
#         buffer.write(await resume.read())

#     pdf_service = PDFExtractionService()

#     extracted_text = pdf_service.extract_text(
#         str(file_path)
#     )

#     return {
#         "filename": resume.filename,
#         "text": extracted_text
#     }


# @router.post("/parse")
# async def parse_resume(
#     resume: UploadFile = File(...)
# ):
#     file_path = UPLOAD_DIR / resume.filename

#     with open(file_path, "wb") as buffer:
#         buffer.write(await resume.read())

#     pdf_service = PDFExtractionService()

#     resume_text = pdf_service.extract_text(
#         str(file_path)
#     )

#     parser = ResumeParserService()

#     parsed_resume = await parser.parse_resume(
#         resume_text
#     )

#     normalised = normalize_resume(parsed_resume)

#     resume = ResumeDocument.model_validate(
#         normalised
#     )
#     return parse_llm_json(
#         resume
#     )
