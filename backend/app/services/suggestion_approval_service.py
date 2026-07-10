from app.agents.inventory_update_agent import (
    update_inventory_from_approvals
)

def approve_suggestions(
    suggestions,
    approved_ids
):

    return (
        update_inventory_from_approvals(
            suggestions,
            approved_ids
        )
    )