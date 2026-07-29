
"""
Review API

Human-in-the-loop endpoints for reviewing and refining a tailored resume
after the initial workflow run.

GET  /api/v1/review/{run_id}                Fetch the stored run.
POST /api/v1/review/{run_id}/section-edit   Direct dot-path edit, no LLM.
POST /api/v1/review/{run_id}/revise         Re-tailor with approved suggestions.
POST /api/v1/review/{run_id}/finalize       Mark the run as finalized (locks
                                             further section-edits in the UI;
                                             not enforced server-side, just a
                                             status flag for the frontend).
"""

import json
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.schemas.candidate_suggestion import CandidateSuggestion
from app.schemas.resume import ResumeDocument
from app.services.resume_revision_service import regenerate_tailored_resume
from app.services.runStore_service import apply_dot_path, clear_all_runs, delete_run, load_run, save_run, list_runs

router = APIRouter(
    prefix="/api/v1/review",
    tags=["Review"],
)


def _get_run_or_404(run_id: str) -> dict[str, Any]:

    run = load_run(run_id)

    if run is None:
        raise HTTPException(
            status_code=404,
            detail=f"No stored run found for run_id={run_id}",
        )

    return run


@router.get("/runs")
def get_runs():
    return list_runs()


@router.get("/{run_id}")
def get_run(run_id: str):
    return _get_run_or_404(run_id)


class SectionEditRequest(BaseModel):
    path: str
    value: Any


@router.post("/{run_id}/section-edit")
def edit_section(run_id: str, request: SectionEditRequest):

    run = _get_run_or_404(run_id)

    resume_dict = run.get("tailored_resume")

    if resume_dict is None:
        raise HTTPException(
            status_code=400,
            detail="This run has no tailored resume yet.",
        )

    resume_dict = dict(resume_dict)

    try:
        apply_dot_path(resume_dict, request.path, request.value)
    except (KeyError, IndexError, TypeError) as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid path '{request.path}': {exc}",
        )

    try:
        resume = ResumeDocument.model_validate(resume_dict)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Edit produced an invalid resume: {exc}",
        )

    run["tailored_resume"] = resume.model_dump(mode="json")

    save_run(run_id, run)

    return {"tailored_resume": resume}


@router.post("/{run_id}/revise")
def revise_resume(run_id: str):

    run = _get_run_or_404(run_id)

    suggestions = CandidateSuggestion.model_validate(
        run.get("candidate_suggestions") or {"suggestions": []}
    )

    approved = [s for s in suggestions.suggestions if s.status == "approved"]

    if not approved:
        raise HTTPException(
            status_code=400,
            detail=(
                "No approved suggestions to apply. Approve suggestions "
                "via /api/v1/suggestions/approve first, or use "
                "/section-edit for direct changes that don't need the LLM."
            ),
        )

    current_resume = run.get("tailored_resume") or run.get("parsed_resume")

    if current_resume is None:
        raise HTTPException(
            status_code=400,
            detail="This run has no resume to revise.",
        )

    revised = regenerate_tailored_resume(
        resume_json=json.dumps(current_resume, indent=2, ensure_ascii=False),
        job_description_json=json.dumps(
            run.get("parsed_jd") or {}, indent=2, ensure_ascii=False
        ),
        inventory_json=json.dumps(
            run.get("resume_inventory") or {}, indent=2, ensure_ascii=False
        ),
        approved_suggestions_json=CandidateSuggestion(
            suggestions=approved
        ).model_dump_json(indent=2),
        enhancement_plan_json=json.dumps(
            run.get("enhancement_plan") or {}, indent=2, ensure_ascii=False
        ),
    )

    versions = run.get("tailored_resume_versions") or []
    if current_resume:
        versions.append(current_resume)

    for s in suggestions.suggestions:
        if s.status == "approved":
            s.status = "applied"

    run["tailored_resume"] = revised.model_dump(mode="json")
    run["tailored_resume_versions"] = versions
    run["candidate_suggestions"] = suggestions.model_dump(mode="json")

    save_run(run_id, run)

    return {
        "tailored_resume": revised,
        "applied_suggestions": approved,
    }


@router.post("/{run_id}/finalize")
def finalize_run(run_id: str):

    run = _get_run_or_404(run_id)

    run["finalized"] = True

    save_run(run_id, run)

    return {"finalized": True}



@router.delete("/runs")
def clear_history():
    """Delete every stored run. Irreversible."""
    deleted = clear_all_runs()
    return {"deleted_count": deleted}


@router.delete("/{run_id}")
def delete_single_run(run_id: str):
    _get_run_or_404(run_id)  # 404 if it doesn't exist
    delete_run(run_id)
    return {"deleted": True, "run_id": run_id}


# """
# Review API

# Human-in-the-loop endpoints for reviewing and refining a tailored resume
# after the initial workflow run.

# Endpoints
# ---------

# GET  /api/v1/review/{run_id}
#     Fetch the stored run: original resume, JD, inventory snapshot,
#     enhancement plan, current tailored resume, and candidate suggestions
#     (each with a status: pending / approved / rejected / applied).

# POST /api/v1/review/{run_id}/section-edit
#     Directly overwrite one field of the tailored resume by dot-path, no
#     LLM call. For quick manual fixes (typo in a bullet, adjust dates, etc).

# POST /api/v1/review/{run_id}/revise
#     Re-run the tailor LLM once more, this time with all currently-approved
#     suggestions injected as USER-APPROVED SUGGESTIONS (which the prompt is
#     already instructed to incorporate). Approved suggestions are marked
#     "applied" afterwards so a later revise call doesn't reapply them.
# """

# import json
# from typing import Any

# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel

# from app.schemas.candidate_suggestion import CandidateSuggestion
# from app.schemas.resume import ResumeDocument
# from app.services.resume_revision_service import regenerate_tailored_resume
# from app.services.runStore_service import apply_dot_path, load_run, save_run

# router = APIRouter(
#     prefix="/api/v1/review",
#     tags=["Review"],
# )


# def _get_run_or_404(run_id: str) -> dict[str, Any]:

#     run = load_run(run_id)

#     if run is None:
#         raise HTTPException(
#             status_code=404,
#             detail=f"No stored run found for run_id={run_id}",
#         )

#     return run


# @router.get("/{run_id}")
# def get_run(run_id: str):
#     """
#     Everything the review UI needs to render a draft + suggestion list.
#     """

#     return _get_run_or_404(run_id)


# class SectionEditRequest(BaseModel):
#     """
#     Dot-path edit against the stored tailored resume, e.g.:

#         {"path": "professional_summary.content", "value": "New summary..."}
#         {"path": "professional_experience.0.responsibilities.2", "value": "Edited bullet"}
#         {"path": "professional_experience.0.projects.1.bullet_points", "value": ["...", "..."]}
#     """

#     path: str
#     value: Any


# @router.post("/{run_id}/section-edit")
# def edit_section(run_id: str, request: SectionEditRequest):

#     run = _get_run_or_404(run_id)

#     resume_dict = run.get("tailored_resume")

#     if resume_dict is None:
#         raise HTTPException(
#             status_code=400,
#             detail="This run has no tailored resume yet.",
#         )

#     resume_dict = dict(resume_dict)

#     try:
#         apply_dot_path(resume_dict, request.path, request.value)
#     except (KeyError, IndexError, TypeError) as exc:
#         raise HTTPException(
#             status_code=400,
#             detail=f"Invalid path '{request.path}': {exc}",
#         )

#     # Re-validate before persisting so a bad edit can't corrupt the run.
#     try:
#         resume = ResumeDocument.model_validate(resume_dict)
#     except Exception as exc:
#         raise HTTPException(
#             status_code=400,
#             detail=f"Edit produced an invalid resume: {exc}",
#         )

#     run["tailored_resume"] = resume.model_dump(mode="json")

#     save_run(run_id, run)

#     return {"tailored_resume": resume}


# @router.post("/{run_id}/revise")
# def revise_resume(run_id: str):

#     run = _get_run_or_404(run_id)

#     suggestions = CandidateSuggestion.model_validate(
#         run.get("candidate_suggestions") or {"suggestions": []}
#     )

#     approved = [
#         s for s in suggestions.suggestions
#         if s.status == "approved"
#     ]

#     if not approved:
#         raise HTTPException(
#             status_code=400,
#             detail=(
#                 "No approved suggestions to apply. Approve suggestions "
#                 "via /api/v1/suggestions/approve first, or use "
#                 "/section-edit for direct changes that don't need the LLM."
#             ),
#         )

#     current_resume = run.get("tailored_resume") or run.get("parsed_resume")

#     if current_resume is None:
#         raise HTTPException(
#             status_code=400,
#             detail="This run has no resume to revise.",
#         )

#     revised = regenerate_tailored_resume(
#         resume_json=json.dumps(current_resume, indent=2, ensure_ascii=False),
#         job_description_json=json.dumps(
#             run.get("parsed_jd") or {}, indent=2, ensure_ascii=False
#         ),
#         inventory_json=json.dumps(
#             run.get("resume_inventory") or {}, indent=2, ensure_ascii=False
#         ),
#         approved_suggestions_json=CandidateSuggestion(
#             suggestions=approved
#         ).model_dump_json(indent=2),
#         enhancement_plan_json=json.dumps(
#             run.get("enhancement_plan") or {}, indent=2, ensure_ascii=False
#         ),
#     )

#     # Keep a version history so a bad revise can be inspected/rolled back.
#     versions = run.get("tailored_resume_versions") or []
#     if current_resume:
#         versions.append(current_resume)

#     for s in suggestions.suggestions:
#         if s.status == "approved":
#             s.status = "applied"

#     run["tailored_resume"] = revised.model_dump(mode="json")
#     run["tailored_resume_versions"] = versions
#     run["candidate_suggestions"] = suggestions.model_dump(mode="json")

#     save_run(run_id, run)

#     return {
#         "tailored_resume": revised,
#         "applied_suggestions": approved,
#     }
