# from pathlib import Path
# import uuid

# from fastapi import (
#     APIRouter,
#     File,
#     Form,
#     UploadFile,
# )

# from app.core.constants import (
#     UPLOAD_DIR
# )

# from app.api.tailor import (
#     validate_pdf,
#     save_upload_file,
# )

# from app.workflows.resume_tailor_graph import (
#     resume_tailor_graph
# )

# from app.services.runStore_service import (
#     save_run
# )

# router = APIRouter(
#     prefix="/api/v1",
#     tags=["Resume Workflow"]
# )


# def _dump(value):
#     """model_dump(mode='json') if it's a pydantic model, else pass through."""
#     return value.model_dump(mode="json") if value is not None else None


# @router.post(
#     "/resume-workflow"
# )
# async def resume_workflow(
#     resume_file: UploadFile = File(...),
#     jd_text: str = Form(...)
# ):

#     validate_pdf(
#         resume_file
#     )

#     file_path = await save_upload_file(
#         resume_file
#     )

#     run_id = str(uuid.uuid4())

#     result = await (
#         resume_tailor_graph.ainvoke(
#             {
#                 "run_id": run_id,

#                 "resume_pdf_path":
#                     str(file_path),

#                 "jd_text":
#                     jd_text,

#                 "parsed_resume":
#                     None,

#                 "parsed_jd":
#                     None,

#                 "gap_analysis":
#                     None,

#                 "tailored_resume":
#                     None,

#                 "validation_result":
#                     None,

#                 "comparison_data":
#                     None,

#                 "retry_count":
#                     0,

#                 "error":
#                     None
#             },
#             config={
#                 "configurable": {
#                     "thread_id": run_id  # If using LangGraph persistence memory
#                 },
#                 "metadata": {
#                     "run_id": run_id,
#                     "environment": "development"
#                 },
#                 "run_name": "Resume_Workflow_API"  # This is the title you will see in LangSmith
#             }
#         )
#     )

#     # ------------------------------------------------------------
#     # Persist the run so /api/v1/review/{run_id} and
#     # /api/v1/review/{run_id}/revise can find it afterward.
#     # ------------------------------------------------------------

#     save_run(
#         run_id,
#         {
#             "resume_pdf_path": str(file_path),
#             "jd_text": jd_text,
#             "parsed_resume": _dump(result.get("parsed_resume")),
#             "parsed_jd": _dump(result.get("parsed_jd")),
#             "resume_inventory": _dump(result.get("resume_inventory")),
#             "gap_analysis": _dump(result.get("gap_analysis")),
#             "enhancement_plan": _dump(result.get("enhancement_plan")),
#             "tailored_resume": _dump(result.get("tailored_resume")),
#             "validation_result": _dump(result.get("validation_result")),
#             "comparison_data": _dump(result.get("comparison_data")),
#             "candidate_suggestions": (
#                 _dump(result.get("candidate_suggestions"))
#                 or {"suggestions": []}
#             ),
#             "tailored_resume_versions": [],
#         },
#     )

#     return {
#         "success": True,
#         "run_id": run_id,
#         "parsed_resume": result["parsed_resume"],
#         "tailored_resume": result["tailored_resume"],
#         "gap_analysis": result["gap_analysis"],
#         "comparison_data": result["comparison_data"],
#         "validation_result": result["validation_result"],
#         "candidate_suggestions": result.get("candidate_suggestions"),
#     }

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

from app.services.runStore_service import (
    save_run
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
    jd_text: str = Form(...)
):

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
                "run_name": "Resume_Workflow_API"  # This is the title you will see in LangSmith
            }
        )
    )

    # return {
    #     "success": True,
    #     "gap_analysis": result["gap_analysis"],
    #     "tailored_resume": result["tailored_resume"],
    #     "comparison": result["comparison_data"]
    # }
    return {
        "success": True,
        "run_id": run_id,
        "parsed_resume": result["parsed_resume"],
        "tailored_resume": result["tailored_resume"],
        "gap_analysis": result["gap_analysis"],
        "comparison_data": result["comparison_data"],
        "validation_result": result["validation_result"],
        "candidate_suggestions": result.get("candidate_suggestions"),
    }