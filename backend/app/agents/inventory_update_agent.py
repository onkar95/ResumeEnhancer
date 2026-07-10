
from datetime import datetime

from app.schemas.candidate_suggestion import (
    CandidateSuggestion
)

from app.services.inventory_service import (
    get_inventory,
    persist_inventory,
    add_skill,
    add_evidence
)

def update_inventory_from_approvals(
    suggestions: CandidateSuggestion,
    approved_ids: list[str]
):

    inventory = get_inventory()

    approved_count = 0

    for suggestion in suggestions.suggestions:

        if (
            suggestion.suggestion_id
            not in approved_ids
        ):
            continue

        approved_count += 1

        suggestion.status = (
            "approved"
        )

        if (
            suggestion.section.lower()
            ==
            "skills"
        ):

            add_skill(
                inventory,
                suggestion.suggested_content
            )

            add_evidence(
                inventory,
                skill_name=
                    suggestion.suggested_content,

                source=
                    (
                        f"User approved "
                        f"suggestion "
                        f"{suggestion.suggestion_id}"
                    )
            )

    inventory.updated_at = (
        datetime.utcnow()
    )

    persist_inventory(
        inventory
    )

    return {
        "approved_count":
            approved_count,

        "inventory":
            inventory
    }


# 
# from datetime import datetime
# from uuid import uuid4

# from app.workflows.state import (
#     ResumeTailorState
# )

# from app.schemas.resume_inventory import (
#     InventorySkill,
#     InventoryEvidence
# )

# from app.services.inventory_storage_service import (
#     InventoryStorageService
# )


# def inventory_update_node(
#     state: ResumeTailorState
# ):

#     inventory = (
#         InventoryStorageService
#         .load_inventory()
#     )

#     suggestions = (
#         state[
#             "approved_suggestions"
#         ]
#     )

#     for suggestion in (
#         suggestions.suggestions
#     ):

#         if (
#             suggestion.status
#             != "approved"
#         ):
#             continue

#         if (
#             suggestion.section
#             == "skill"
#         ):

#             inventory.skills.append(
#                 InventorySkill(
#                     name=suggestion.suggested_content,
#                     rating=(
#                         suggestion.user_rating
#                         or 5
#                     ),
#                     verified=True,
#                     source="user_confirmed"
#                 )
#             )

#         inventory.evidence.append(
#             InventoryEvidence(
#                 evidence_id=str(uuid4()),
#                 title=(
#                     suggestion.suggested_content
#                 ),
#                 section=(
#                     suggestion.section
#                 ),
#                 content=(
#                     suggestion.user_edited_content
#                     or
#                     suggestion.suggested_content
#                 ),
#                 source="user_approved",
#                 created_at=datetime.utcnow()
#             )
#         )

#     InventoryStorageService.save_inventory(
#         inventory
#     )

#     return {
#         "resume_inventory": inventory
#     }