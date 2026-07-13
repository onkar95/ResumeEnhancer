from app.utils.skill_normalizer import normalize_skill
from app.workflows.state import (
    ResumeTailorState
)

from app.schemas.gap_analysis import (
    GapAnalysis
)
from app.core.logger import logger


def extract_resume_skills(resume):

    skills = set()

    for category in (
        resume.technical_skills.categories
    ):

        for skill in category.skills:

            # skills.add(
            #     skill.strip().lower()
            # )
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


def gap_analysis_node(
    state: ResumeTailorState
):
    logger.info("started gap_analysis-agent")

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
    logger.info(
        "resume_skills=%s",
        sorted(resume_skills)
    )

    inventory_skills = (
        extract_inventory_skills(
            inventory
        )
    )
    logger.info(
        "inventory_skills=%s",
        sorted(inventory_skills)
    )

    jd_skills = {
        normalize_skill(skill)

        for skill in (
            jd.required_skills
            + jd.preferred_skills
        )

        if skill.strip()
    }

    logger.info(
        "jd_skills=%s",
        sorted(jd_skills)
    )
    already_present = []

    available_in_inventory = []

    missing_and_unknown = []

    for skill in jd_skills:

        if skill in resume_skills:

            already_present.append(
                skill
            )

        elif skill in inventory_skills:

            available_in_inventory.append(
                skill
            )

        else:

            missing_and_unknown.append(
                skill
            )

    matched_keywords = []

    missing_keywords = []

    for keyword in jd.keywords:

        # keyword = (
        #     keyword.strip()
        #     .lower()
        # )
        keyword = normalize_skill(
            keyword
        )

        if (
            keyword in resume_skills
            or keyword in inventory_skills
        ):

            matched_keywords.append(
                keyword
            )

        else:

            missing_keywords.append(
                keyword
            )



    result = GapAnalysis(

        already_present=already_present,

        available_in_inventory=available_in_inventory,

        missing_and_unknown=missing_and_unknown,

        matched_keywords=matched_keywords,

        missing_keywords=missing_keywords,

    )

    print("gap_analysis ", "=" * 100)
    print("", result)  # Print the last 3000 characters
    print("=" * 100)

    return {
        "gap_analysis":
            result
    }
