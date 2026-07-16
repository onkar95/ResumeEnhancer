from app.utils.skill_normalizer import (
    normalize_skill
)

from app.workflows.state import (
    ResumeTailorState
)

from app.schemas.gap_analysis import (
    GapAnalysis
)

from app.core.logger import logger


def extract_resume_skills(
    resume
):

    skills = set()

    for category in (
        resume.technical_skills.categories
    ):
        for skill in category.skills:
            skills.add(
                normalize_skill(skill)
            )

    return skills


def extract_inventory_skills(
    inventory
):

    return {
        normalize_skill(skill.name)
        for skill in inventory.skills
    }


def extract_summary_text(
    inventory
):

    values = []

    values.extend(
        inventory.summary_points
    )

    values.extend(
        inventory.summary_keywords
    )

    return " ".join(values).lower()


# def find_relevant_experience(
#     inventory,
#     jd_keywords
# ):

#     results = []

#     for exp in inventory.professional_experience:

#         searchable_text = []

#         searchable_text.append(
#             exp.role
#         )

#         searchable_text.append(
#             exp.company
#         )

#         searchable_text.extend(
#             exp.responsibilities
#         )

#         combined = (
#             " ".join(
#                 searchable_text
#             ).lower()
#         )

#         matches = 0

#         for keyword in jd_keywords:

#             if keyword in combined:
#                 matches += 1

#         if matches > 0:

#             results.append(
#                 f"{exp.role} @ {exp.company}"
#             )

#     return list(
#         dict.fromkeys(results)
#     )


# def find_relevant_projects(
#     inventory,
#     jd_keywords
# ):

#     results = []

#     for exp in inventory.professional_experience:

#         for project in exp.projects:

#             searchable_text = []

#             searchable_text.append(
#                 project.title
#             )

#             searchable_text.extend(
#                 project.bullet_points
#             )

#             combined = (
#                 " ".join(
#                     searchable_text
#                 ).lower()
#             )

#             matches = 0

#             for keyword in jd_keywords:

#                 if keyword in combined:
#                     matches += 1

#             if matches > 0:

#                 results.append(
#                     project.title
#                 )

#     return list(
#         dict.fromkeys(results)
#     )


def gap_analysis_node(
    state: ResumeTailorState
):

    logger.info(
        "started gap_analysis_agent"
    )

    resume = state[
        "parsed_resume"
    ]

    inventory = state[
        "resume_inventory"
    ]

    jd = state[
        "parsed_jd"
    ]

    resume_skills = (
        extract_resume_skills(
            resume
        )
    )

    inventory_skills = (
        extract_inventory_skills(
            inventory
        )
    )

    jd_skills = {
        normalize_skill(skill)
        for skill in (
            jd.required_skills
            + jd.preferred_skills
        )
        if skill.strip()
    }

    matched_skills = []

    inventory_skill_matches = []

    missing_skills = []

    for skill in jd_skills:

        if skill in resume_skills:

            matched_skills.append(
                skill
            )

        elif skill in inventory_skills:

            inventory_skill_matches.append(
                skill
            )

        else:

            missing_skills.append(
                skill
            )

    matched_keywords = []

    missing_keywords = []

    normalized_keywords = []

    for keyword in jd.keywords:

        normalized = normalize_skill(
            keyword
        )

        normalized_keywords.append(
            normalized
        )

        if (
            normalized in resume_skills
            or normalized in inventory_skills
        ):

            matched_keywords.append(
                normalized
            )

        else:

            missing_keywords.append(
                normalized
            )

    summary_text = (
        extract_summary_text(
            inventory
        )
    )

    summary_opportunities = []

    for skill in (
        matched_skills
        + inventory_skill_matches
    ):

        if skill not in summary_text:

            summary_opportunities.append(
                skill
            )

    # relevant_experience = (
    #     find_relevant_experience(
    #         inventory,
    #         normalized_keywords
    #     )
    # )

    # relevant_projects = (
    #     find_relevant_projects(
    #         inventory,
    #         normalized_keywords
    #     )
    # )

    result = GapAnalysis(

        matched_skills=sorted(
            matched_skills
        ),

        inventory_skills=sorted(
            inventory_skill_matches
        ),

        missing_skills=sorted(
            missing_skills
        ),

        matched_keywords=sorted(
            matched_keywords
        ),

        missing_keywords=sorted(
            missing_keywords
        ),

        # relevant_experience=sorted(
        #     relevant_experience
        # ),

        # relevant_projects=sorted(
        #     relevant_projects
        # ),

        summary_opportunities=sorted(
            list(
                set(
                    summary_opportunities
                )
            )
        )
    )

    logger.info(
        "gap_analysis=%s",
        result.model_dump()
    )

    return {
        "gap_analysis": result
    }
