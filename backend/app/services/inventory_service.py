from datetime import datetime

from app.schemas.resume_inventory import (
    ResumeInventory,
    InventorySkill,
    ResumeVersion,
    InventoryEvidence
)

from app.services.inventory_storage_service import (
    load_inventory,
    save_inventory
)


def get_inventory() -> ResumeInventory:

    return load_inventory()


def persist_inventory(
    inventory: ResumeInventory
):

    save_inventory(
        inventory
    )


def skill_exists(
    inventory: ResumeInventory,
    skill_name: str
) -> bool:

    return any(
        skill.name.lower()
        ==
        skill_name.lower()
        for skill in inventory.skills
    )


def get_skill(
    inventory: ResumeInventory,
    skill_name: str
):

    for skill in inventory.skills:

        if (
            skill.name.lower()
            ==
            skill_name.lower()
        ):
            return skill

    return None


def add_skill(
    inventory: ResumeInventory,
    skill_name: str,
    confidence: float = 1.0,
    evidence: str | None = None
):

    existing = get_skill(
        inventory,
        skill_name
    )

    if existing:
        return inventory

    inventory.skills.append(
        InventorySkill(
            name=skill_name,
            confidence=confidence
        )
    )

    inventory.updated_at = (
        datetime.utcnow()
    )

    return inventory


def get_all_skill_names(
    inventory: ResumeInventory
):

    return [
        skill.name
        for skill in inventory.skills
    ]


def add_summary(
    inventory: ResumeInventory,
    summary: str
):

    if (
        summary
        and
        summary
        not in inventory.summary_points
    ):

        inventory.summary_points.append(
            summary
        )

    return inventory


def add_certification(
    inventory: ResumeInventory,
    certification
):

    inventory.certifications.append(
        certification
    )

    return inventory


def add_experience(
    inventory: ResumeInventory,
    experience
):

    exists = any(

        exp.company.lower()
        ==
        experience.company.lower()

        and

        exp.job_title.lower()
        ==
        experience.job_title.lower()

        for exp in inventory.professional_experience
    )

    if not exists:

        inventory.professional_experience.append(
            experience
        )

    return inventory


def add_resume_version(
    inventory: ResumeInventory,
    version_name: str
):

    inventory.resume_versions.append(

        ResumeVersion(
            version_name=version_name,
            created_at=datetime.utcnow()
        )
    )

    return inventory


def add_evidence(
    inventory: ResumeInventory,
    skill_name: str,
    source: str
):

    skill = get_skill(
        inventory,
        skill_name
    )

    if not skill:
        return inventory

    skill.evidence.append(

        InventoryEvidence(
            source=source
        )
    )

    return inventory
#
# from app.services.inventory_storage_service import (
#     InventoryStorageService
# )


# class InventoryService:

#     @staticmethod
#     def get_skill(skill_name):

#         inventory = (
#             InventoryStorageService
#             .load_inventory()
#         )

#         for skill in inventory.skills:

#             if (
#                 skill.name.lower()
#                 ==
#                 skill_name.lower()
#             ):
#                 return skill

#         return None
