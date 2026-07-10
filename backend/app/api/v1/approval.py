from fastapi import APIRouter

from app.schemas.suggestion_requests import (
    SuggestionApprovalRequest
)

from app.services.suggestion_approval_service import (
    approve_suggestions
)

router = APIRouter(
    prefix="/suggestions",
    tags=["Suggestions"]
)


@router.post(
    "/approve"
)
def approve(
    request:
    SuggestionApprovalRequest
):

    #
    # TODO
    #
    # fetch stored candidate suggestions
    #

    candidate_suggestions = ...

    result = approve_suggestions(

        candidate_suggestions,

        request.suggestion_ids
    )

    return result


# @router.post(
#     "/approve"
# )
# def approve_suggestions(
#     request:
#     SuggestionApprovalRequest
# ):

#     return {

#         "approved":
#             request.suggestion_ids
#     }


@router.post(
    "/reject"
)
def reject_suggestions(
    request:
    SuggestionApprovalRequest
):

    return {

        "rejected":
            request.suggestion_ids
    }
