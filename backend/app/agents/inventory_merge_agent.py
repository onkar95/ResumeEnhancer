from datetime import datetime

from app.workflows.state import ResumeTailorState

from app.schemas.resume_inventory import (
    InventorySkill,
    ResumeVersion
)

from app.services.inventory_storage_service import (
    InventoryStorageService
)

from app.agents.helpers import (
    extract_keywords
)


def normalize(value: str) -> str:

    return (
        value.strip().lower()
        if value
        else ""
    )


def merge_project(
    existing_project,
    incoming_project
):

    existing_bullets = {
        normalize(b)
        for b in (
            existing_project.bullet_points
        )
    }

    for bullet in (
        incoming_project.bullet_points
    ):

        if (
            normalize(bullet)
            not in existing_bullets
        ):

            existing_project.bullet_points.append(
                bullet
            )

            existing_bullets.add(
                normalize(bullet)
            )


def merge_experience(
    existing_exp,
    incoming_exp
):

    existing_responsibilities = {
        normalize(r)
        for r in (
            existing_exp.responsibilities
        )
    }

    for responsibility in (
        incoming_exp.responsibilities
    ):

        if (
            normalize(responsibility)
            not in existing_responsibilities
        ):

            existing_exp.responsibilities.append(
                responsibility
            )

            existing_responsibilities.add(
                normalize(responsibility)
            )

    existing_projects = {
        normalize(project.title): project
        for project in (
            existing_exp.projects
        )
    }

    for incoming_project in (
        incoming_exp.projects
    ):

        project_key = normalize(
            incoming_project.title
        )

        if (
            project_key
            in existing_projects
        ):

            merge_project(
                existing_projects[
                    project_key
                ],
                incoming_project
            )

        else:

            existing_exp.projects.append(
                incoming_project
            )

    if (
        not existing_exp.location
        and incoming_exp.location
    ):
        existing_exp.location = (
            incoming_exp.location
        )

    if (
        not existing_exp.start_date
        and incoming_exp.start_date
    ):
        existing_exp.start_date = (
            incoming_exp.start_date
        )

    if (
        not existing_exp.end_date
        and incoming_exp.end_date
    ):
        existing_exp.end_date = (
            incoming_exp.end_date
        )


def find_matching_experience(
    experience,
    inventory_experiences
):

    for existing in (
        inventory_experiences
    ):

        same_company = (
            normalize(existing.company)
            ==
            normalize(experience.company)
        )

        same_role = (
            normalize(existing.role)
            ==
            normalize(experience.role)
        )

        if (
            same_company
            and same_role
        ):
            return existing

    return None


def inventory_merge_node(
    state: ResumeTailorState
):

    inventory = (
        InventoryStorageService
        .load_inventory()
    )

    resume = state[
        "parsed_resume"
    ]

    # ==================================
    # Professional Summary
    # ==================================

    summary = (
        resume.professional_summary.content
        .strip()
    )

    existing_summaries = {
        normalize(point)
        for point in (
            inventory.summary_points
        )
    }

    if (
        normalize(summary)
        not in existing_summaries
    ):

        inventory.summary_points.append(
            summary
        )

    inventory.summary_keywords = (
        extract_keywords(
            inventory.summary_points
        )
    )

    # ==================================
    # Skills
    # ==================================

    existing_skills = {
        normalize(skill.name)
        for skill in inventory.skills
    }

    for category in (
        resume.technical_skills.categories
    ):

        for skill_name in (
            category.skills
        ):

            if (
                normalize(skill_name)
                not in existing_skills
            ):

                inventory.skills.append(
                    InventorySkill(
                        name=skill_name,
                        rating=5,
                        verified=True,
                        source="resume"
                    )
                )

                existing_skills.add(
                    normalize(skill_name)
                )

    # ==================================
    # Experience
    # ==================================

    for incoming_exp in (
        resume.professional_experience
    ):

        existing_exp = (
            find_matching_experience(
                incoming_exp,
                inventory.professional_experience
            )
        )

        if existing_exp:

            merge_experience(
                existing_exp,
                incoming_exp
            )

        else:

            inventory.professional_experience.append(
                incoming_exp
            )

    # ==================================
    # Certifications
    # ==================================

    existing_certs = {
        normalize(cert.name)
        for cert in (
            inventory.certifications
        )
    }

    for cert in (
        resume.certifications
    ):

        if (
            normalize(cert.name)
            not in existing_certs
        ):

            inventory.certifications.append(
                cert
            )

            existing_certs.add(
                normalize(cert.name)
            )

    # ==================================
    # Education
    # ==================================

    existing_education = {
        (
            normalize(edu.degree),
            normalize(edu.institution)
        )
        for edu in (
            inventory.education
        )
    }

    for edu in (
        resume.education
    ):

        key = (
            normalize(edu.degree),
            normalize(edu.institution)
        )

        if (
            key
            not in existing_education
        ):

            inventory.education.append(
                edu
            )

            existing_education.add(
                key
            )

    # ==================================
    # Resume Versions
    # ==================================

    existing_files = {
        normalize(version.filename)
        for version in (
            inventory.resume_versions
        )
    }

    current_file = normalize(
        state["resume_pdf_path"]
    )

    if (
        current_file
        not in existing_files
    ):

        inventory.resume_versions.append(
            ResumeVersion(
                filename=state[
                    "resume_pdf_path"
                ],
                uploaded_at=datetime.utcnow()
            )
        )

    # ==================================
    # Metadata
    # ==================================

    inventory.updated_at = (
        datetime.utcnow()
    )

    InventoryStorageService.save_inventory(
        inventory
    )

    return {
        "resume_inventory": inventory
    }