from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.schemas.resume import ResumeDocument
from app.services.pdf_export_service import generate_resume_pdf
from app.services.docx_export_service import generate_resume_docx
from app.services.database.DB_service import load_run

router = APIRouter(prefix="/api/v1/review", tags=["Export"])


def _get_resume(run_id: str) -> ResumeDocument:
    run = load_run(run_id)

    if run is None:
        raise HTTPException(status_code=404, detail=f"No run found for {run_id}")

    resume_dict = run.get("tailored_resume") or run.get("parsed_resume")

    if resume_dict is None:
        raise HTTPException(status_code=400, detail="This run has no resume yet.")

    return ResumeDocument.model_validate(resume_dict)


@router.get("/{run_id}/export/pdf")
async def export_pdf(run_id: str):
    resume = _get_resume(run_id)

    pdf_bytes = await generate_resume_pdf(resume)

    filename = f"{resume.name.replace(' ', '_')}_resume.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/{run_id}/export/docx")
def export_docx(run_id: str):
    # unchanged, python-docx is sync and has no native-lib issues
    resume = _get_resume(run_id)
    docx_bytes = generate_resume_docx(resume)

    filename = f"{resume.name.replace(' ', '_')}_resume.docx"

    return Response(
        content=docx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )