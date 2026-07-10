from pathlib import Path

from fastapi import (
    APIRouter,
    File,
    Form,
    UploadFile,
)

from app.core.constants import (
    UPLOAD_DIR
)

from app.api.tailor import (
    validate_pdf,
    save_upload_file,
)

from app.workflows.resume_tailor_graph import (
    resume_tailor_graph
)

router = APIRouter(
    prefix="/api/v1",
    tags=["Resume Workflow"]
)

@router.post(
    "/resume-workflow"
)
async def resume_workflow(
    resume_file: UploadFile = File(...),
    jd_text: str = Form(...)
):

    validate_pdf(
        resume_file
    )

    file_path = await save_upload_file(
        resume_file
    )

    result = await (
        resume_tailor_graph.ainvoke(
            {
                "resume_pdf_path":
                    str(file_path),

                "jd_text":
                    jd_text,

                "parsed_resume":
                    None,

                "parsed_jd":
                    None,

                "gap_analysis":
                    None,

                "tailored_resume":
                    None,

                "validation_result":
                    None,

                "comparison_data":
                    None,

                "retry_count":
                    0,

                "error":
                    None
            }
        )
    )

    return {
        "success": True,
        "gap_analysis":
            result[
                "gap_analysis"
            ],

        "tailored_resume":
            result[
                "tailored_resume"
            ],

        "comparison":
            result[
                "comparison_data"
            ]
    }