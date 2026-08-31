from datetime import datetime, UTC
from pathlib import Path
import uuid

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

from app.services.DB_service import (

    save_run
)
from fastapi import Depends, HTTPException

from app.dependencies import get_current_user
from app.services.usage_service import (
    has_quota,
    record_generation,
    remaining_quota,
)


router = APIRouter(
    prefix="/api/v1",
    tags=["Resume Workflow"]
)


def _dump(value):
    """model_dump(mode='json') if it's a pydantic model, else pass through."""
    return value.model_dump(mode="json") if value is not None else None


@router.post(
    "/resume-workflow"
)
async def resume_workflow(
    resume_file: UploadFile = File(...),
    jd_text: str = Form(...),
    user_instructions: str = Form(""),
     current_user: dict = Depends(get_current_user),
):
    if not has_quota(current_user["user_id"]):
        raise HTTPException(
            status_code=429,
            detail=(
                "You've reached your limit of 2 resume generations per "
                "24 hours. Please try again later."
            ),
        )


    validate_pdf(
        resume_file
    )

    file_path = await save_upload_file(
        resume_file
    )

    run_id = str(uuid.uuid4())

    result = await (
        resume_tailor_graph.ainvoke(
            {
                "run_id": run_id,

                "resume_pdf_path":
                    str(file_path),

                "jd_text":
                    jd_text,

                "user_instructions":
                    user_instructions or "",

                "user_context":
                    None,

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
            },
            config={
                "configurable": {
                    "thread_id": run_id
                },
                "metadata": {
                    "run_id": run_id,
                    "environment": "development"
                },
                "run_name": "Resume_Workflow_API"
            }
        )
    )

    # ------------------------------------------------------------
    # Persist the run so /api/v1/review/{run_id} and
    # /api/v1/review/{run_id}/revise|finalize can find it afterward.
    # ------------------------------------------------------------

    initial_chat_history = []

    if user_instructions and user_instructions.strip():
        initial_chat_history = [
            {
                "role": "user",
                "content": user_instructions.strip(),
                "created_at": datetime.utcnow().isoformat(),
            },
            {
                "role": "assistant",
                "content": "Applied these notes to the initial tailored resume.",
                "created_at": datetime.utcnow().isoformat(),
            },
        ]

    save_run(
        run_id,
        {
            "user_id": current_user["user_id"],
            "resume_pdf_path": str(file_path),
            "jd_text": jd_text,
            "chat_history": initial_chat_history,
            "revision_count": 0,
            "parsed_resume": _dump(result.get("parsed_resume")),
            "user_instructions": user_instructions or "",
            "user_context": _dump(result.get("user_context")),
            "resume_inventory": _dump(result.get("resume_inventory")),
            "gap_analysis": _dump(result.get("gap_analysis")),
            "enhancement_plan": _dump(result.get("enhancement_plan")),
            "tailored_resume": _dump(result.get("tailored_resume")),
            "validation_result": _dump(result.get("validation_result")),
            "comparison_data": _dump(result.get("comparison_data")),
            "candidate_suggestions": (
                _dump(result.get("candidate_suggestions"))
                or {"suggestions": []}
            ),
            "tailored_resume_versions": [],
            "finalized": False,
            "created_at": datetime.utcnow().isoformat(),
            "resume_name": resume_file.filename,
        },
    )

    record_generation(current_user["user_id"], run_id)
      
    return {
        "success": True,
        "run_id": run_id, 
        "remaining_quota": remaining_quota(current_user["user_id"]),
        "parsed_resume": result["parsed_resume"],
        "tailored_resume": result["tailored_resume"],
        "gap_analysis": result["gap_analysis"],
        "comparison_data": result["comparison_data"],
        "validation_result": result["validation_result"],
        "candidate_suggestions": result.get("candidate_suggestions"),
        "user_instructions": user_instructions or "",
    }
