
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

from datetime import datetime, timezone
import json
from typing import Any


from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.core.constants import MAX_CHAT_REVISIONS
from app.schemas.chat import ChatReviseRequest
from app.schemas.resume_inventory import ResumeInventory
from app.services.inventory_service import merge_declared_skills
from app.services.user_context_service import extract_user_context
from app.schemas.candidate_suggestion import CandidateSuggestion
from app.schemas.resume import ResumeDocument
from app.services.resume_revision_service import regenerate_tailored_resume
from app.services.DB_service import apply_dot_path, clear_all_runs, delete_run, load_run, save_run, list_runs

from app.dependencies import get_current_user

router = APIRouter(
    prefix="/api/v1/review",
    tags=["Review"],
)



def _get_run_or_404(run_id: str, user_id: str) -> dict[str, Any]:
    run = load_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail=f"No stored run found for run_id={run_id}")
    if run.get("user_id") and run["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="You don't have access to this run.")
    return run

@router.get("/runs")
def get_runs(current_user: dict = Depends(get_current_user)):
    return [r for r in list_runs() if r.get("user_id") == current_user["user_id"]]
    # (or push the filter into list_runs() as a mongo query — cheaper at scale)

@router.get("/{run_id}")
def get_run(run_id: str, current_user: dict = Depends(get_current_user)):
    return _get_run_or_404(run_id, current_user["user_id"])


# new route -- place with the other /{run_id}/... routes, after /revise


@router.post("/{run_id}/chat")
def chat_revise(run_id: str, request: ChatReviseRequest,current_user: dict = Depends(get_current_user),):

    run = _get_run_or_404(run_id,current_user["user_id"])

    message = request.message.strip()

    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    revision_count = run.get("revision_count", 0)

    if revision_count >= MAX_CHAT_REVISIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Maximum of {MAX_CHAT_REVISIONS} chat revisions reached "
                f"for this run."
            ),
        )

    current_resume = run.get("tailored_resume") or run.get("parsed_resume")

    if current_resume is None:
        raise HTTPException(
            status_code=400,
            detail="This run has no resume to revise.",
        )

    chat_history = run.get("chat_history") or []

    # Combine this message with prior user turns so the model has the full
    # thread of intent, not just the latest line in isolation.
    past_user_messages = [
        m["content"] for m in chat_history if m.get("role") == "user"
    ]

    combined_instructions = "\n".join(past_user_messages + [message])

    user_context = extract_user_context(combined_instructions)

    inventory = ResumeInventory.model_validate(
        run.get("resume_inventory") or {}
    )

    inventory = merge_declared_skills(inventory, user_context)

    revised = regenerate_tailored_resume(
        resume_json=json.dumps(current_resume, indent=2, ensure_ascii=False),
        job_description_json=json.dumps(
            run.get("parsed_jd") or {}, indent=2, ensure_ascii=False
        ),
        inventory_json=inventory.model_dump_json(indent=2),
        approved_suggestions_json="{}",
        enhancement_plan_json=json.dumps(
            run.get("enhancement_plan") or {}, indent=2, ensure_ascii=False
        ),
        user_context_json=user_context.model_dump_json(indent=2),
    )

    versions = run.get("tailored_resume_versions") or []
    versions.append(current_resume)

    now = datetime.now(timezone.utc).isoformat()

    chat_history.append(
        {"role": "user", "content": message, "created_at": now})
    chat_history.append(
        {
            "role": "assistant",
            "content": "Updated your tailored resume based on this message.",
            "created_at": now,
        }
    )

    run["tailored_resume"] = revised.model_dump(mode="json")
    run["tailored_resume_versions"] = versions
    run["chat_history"] = chat_history
    run["revision_count"] = revision_count + 1
    run["resume_inventory"] = inventory.model_dump(mode="json")
    run["user_context"] = user_context.model_dump(mode="json")

    save_run(run_id, run)

    return {
        "tailored_resume": revised,
        "chat_history": chat_history,
        "revision_count": run["revision_count"],
        "remaining_revisions": MAX_CHAT_REVISIONS - run["revision_count"],
    }


class SectionEditRequest(BaseModel):
    path: str
    value: Any
    user_id:str


@router.post("/{run_id}/section-edit")
def edit_section(run_id: str, request: SectionEditRequest):

    run = _get_run_or_404(run_id,request.user_id)

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
def revise_resume(run_id: str,current_user: dict = Depends(get_current_user)):

    run = _get_run_or_404(run_id, current_user["user_id"])

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
        user_context_json=json.dumps(
            run.get("user_context") or {}, indent=2, ensure_ascii=False
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
def finalize_run(run_id: str,current_user: dict = Depends(get_current_user)):

    run = _get_run_or_404(run_id, current_user["user_id"])

    run["finalized"] = True

    save_run(run_id, run)

    return {"finalized": True}


@router.delete("/runs")
def clear_history():
    """Delete every stored run. Irreversible."""
    deleted = clear_all_runs()
    return {"deleted_count": deleted}


@router.delete("/{run_id}")
def delete_single_run(run_id: str,current_user: dict = Depends(get_current_user)):
    _get_run_or_404(run_id, current_user["user_id"])  # 404 if it doesn't exist
    delete_run(run_id)
    return {"deleted": True, "run_id": run_id}


