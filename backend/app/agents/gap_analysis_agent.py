from app.workflows.state import (
    ResumeTailorState
)

from app.schemas.gap_analysis import (
    GapAnalysis
)


def extract_resume_skills(resume):

    skills = set()

    for category in (
        resume.technical_skills.categories
    ):

        for skill in category.skills:

            skills.add(
                skill.strip().lower()
            )

    return skills


def extract_inventory_skills(
    inventory
):

    return {
        skill.name.strip().lower()
        for skill in inventory.skills
    }


def gap_analysis_node(
    state: ResumeTailorState
):

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

        skill.strip().lower()

        for skill in (
            jd.required_skills
            + jd.preferred_skills
        )

        if skill.strip()
    }

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

        keyword = (
            keyword.strip()
            .lower()
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

    total_keywords = (
        len(jd_skills)
        + len(jd.keywords)
    )

    matched = (
        len(already_present)
        + len(available_in_inventory)
        + len(matched_keywords)
    )

    ats_before = 0

    if total_keywords:

        ats_before = int(
            (matched / total_keywords)
            * 100
        )

    result = GapAnalysis(

        already_present=
            already_present,

        available_in_inventory=
            available_in_inventory,

        missing_and_unknown=
            missing_and_unknown,

        matched_keywords=
            matched_keywords,

        missing_keywords=
            missing_keywords,

        ats_before=
            ats_before,

        ats_after=
            ats_before
    )

    return {
        "gap_analysis":
            result
    }