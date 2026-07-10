from fastapi import APIRouter

from app.services.inventory_service import (
    get_inventory
)

from app.schemas.responses import (
    InventoryResponse
)

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)


@router.get(
    "",
    response_model=
        InventoryResponse
)
def fetch_inventory():

    inventory = (
        get_inventory()
    )

    return InventoryResponse(
        inventory=inventory
    )


@router.get(
    "/skills"
)
def get_skills():

    inventory = (
        get_inventory()
    )

    return {

        "skills": [

            skill.name

            for skill in inventory.skills
        ]
    }