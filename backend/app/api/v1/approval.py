from fastapi import APIRouter, HTTPException

from app.schemas.suggestion_requests import (
    SuggestionApprovalRequest
)

from app.schemas.candidate_suggestion import (
    CandidateSuggestion
)

from app.services.runStore_service import (
    load_run,
    save_run,
)

router = APIRouter(
    prefix="/api/v1/suggestions",
    tags=["Suggestions"]
)


def _load_suggestions(run_id: str) -> tuple[dict, CandidateSuggestion]:

    run = load_run(run_id)

    if run is None:
        raise HTTPException(
            status_code=404,
            detail=f"No stored run found for run_id={run_id}",
        )

    suggestions = CandidateSuggestion.model_validate(
        run.get("candidate_suggestions") or {"suggestions": []}
    )

    return run, suggestions


@router.post(
    "/approve"
)
def approve(
    request: SuggestionApprovalRequest
):

    run, suggestions = _load_suggestions(request.run_id)

    approved_count = 0

    for suggestion in suggestions.suggestions:

        if suggestion.suggestion_id in request.suggestion_ids:
            suggestion.status = "approved"
            approved_count += 1

    run["candidate_suggestions"] = suggestions.model_dump(mode="json")

    save_run(request.run_id, run)

    return {
        "approved_count": approved_count,
        "candidate_suggestions": suggestions,
    }


@router.post(
    "/reject"
)
def reject_suggestions(
    request: SuggestionApprovalRequest
):

    run, suggestions = _load_suggestions(request.run_id)

    rejected_count = 0

    for suggestion in suggestions.suggestions:

        if suggestion.suggestion_id in request.suggestion_ids:
            suggestion.status = "rejected"
            rejected_count += 1

    run["candidate_suggestions"] = suggestions.model_dump(mode="json")

    save_run(request.run_id, run)

    return {
        "rejected_count": rejected_count,
        "candidate_suggestions": suggestions,
    }