from datetime import datetime

from app.schemas.resume_inventory import (
    ResumeInventory,
    InventorySkill,
    ResumeVersion,
    InventoryEvidence
)

from app.services.inventory_storage_service import (
    InventoryStorageService
)


from app.schemas.user_context import UserContext
from app.utils.skill_normalizer import normalize_skill


def get_inventory() -> ResumeInventory:

    return InventoryStorageService.load_inventory()


def persist_inventory(
    inventory: ResumeInventory
):

    InventoryStorageService.save_inventory(
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


def merge_declared_skills(
    inventory: ResumeInventory,
    user_context: UserContext | None
) -> ResumeInventory:
    """
    Folds any candidate-declared skills (from the optional notes box or a
    chat message) into the inventory, same rule as the resume-skill merge:
    skip if already present (normalized).
    """

    if not user_context or not user_context.declared_skills:
        return inventory

    existing = {
        normalize_skill(skill.name)
        for skill in inventory.skills
    }

    for declared in user_context.declared_skills:

        normalized = normalize_skill(declared.skill)

        if not normalized or normalized in existing:
            continue

        inventory.skills.append(
            InventorySkill(
                name=declared.skill,
                rating=max(1, round(declared.confidence * 5)),
                verified=False,
                source="user_declared"
            )
        )

        existing.add(normalized)

    inventory.updated_at = datetime.utcnow()

    return inventory


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
#             .InventoryStorageService.load_inventory()
#         )

#         for skill in inventory.skills:

#             if (
#                 skill.name.lower()
#                 ==
#                 skill_name.lower()
#             ):
#                 return skill

#         return None
