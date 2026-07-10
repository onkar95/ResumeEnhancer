import json

from pathlib import Path

from app.schemas.resume_inventory import (
    ResumeInventory
)

INVENTORY_FILE = Path(
    "app/data/resume_inventory.json"
)


class InventoryStorageService:

    @staticmethod
    def load_inventory():

        if not INVENTORY_FILE.exists():

            return ResumeInventory()

        try:

            with open(
                INVENTORY_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                content = f.read().strip()

            # empty file
            if not content:

                return ResumeInventory()

            data = json.loads(content)

            return (
                ResumeInventory
                .model_validate(data)
            )

        except (
            json.JSONDecodeError,
            ValueError
        ):

            print(
                f"Invalid inventory file: "
                f"{INVENTORY_FILE}"
            )

            return ResumeInventory()

    @staticmethod
    def save_inventory(
        inventory: ResumeInventory
    ):

        INVENTORY_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            INVENTORY_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                inventory.model_dump(
                    mode="json"
                ),
                f,
                indent=2
            )