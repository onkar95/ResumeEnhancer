
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


