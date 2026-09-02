
from app.utils.skill_normalizer import (
    normalize_skill
)

from app.utils.text_matching import (
    resume_inventory_text,
    keyword_in_text,
    match_keywords,
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


def find_relevant_experience(
    inventory,
    jd_terms
):
    """
    Surfaces experience entries from the INVENTORY (which may include
    roles/companies not currently on the resume being tailored) that are
    relevant to this JD, based on JD skills + keywords appearing in the
    role/company/responsibilities text.
    """

    results = []

    for exp in inventory.professional_experience:

        text = " ".join(
            filter(
                None,
                [exp.role, exp.company] + list(exp.responsibilities or [])
            )
        ).lower()

        if any(
            keyword_in_text(term, text)
            for term in jd_terms
        ):
            results.append(
                f"{exp.role} @ {exp.company}"
            )

    return list(dict.fromkeys(results))


def find_relevant_projects(
    inventory,
    jd_terms
):
    """
    Same idea as find_relevant_experience but at the project level, so the
    tailor prompt can be told "this project from the inventory is worth
    pulling forward even though it's buried under a different job".
    """

    results = []

    for exp in inventory.professional_experience:

        for project in exp.projects:

            text = " ".join(
                filter(
                    None,
                    [project.title]
                    + list(project.bullet_points or [])
                    + list(getattr(project, "technologies", None) or [])
                )
            ).lower()

            if any(
                keyword_in_text(term, text)
                for term in jd_terms
            ):
                results.append(
                    project.title
                )

    return list(dict.fromkeys(results))


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

    # --------------------------------------------------
    # Skills: matched as normalized tokens against the
    # technical_skills sections (resume vs inventory).
    # --------------------------------------------------

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
            matched_skills.append(skill)

        elif skill in inventory_skills:
            inventory_skill_matches.append(skill)

        else:
            missing_skills.append(skill)

    # --------------------------------------------------
    # Keywords: these are free-text phrases from the JD
    # ("deployment pipelines", "operational excellence"),
    # NOT skill tokens. They must be searched across the
    # full resume text, same as an ATS scanner would --
    # matching them against a skills-only set (the old bug)
    # made them permanently "missing" no matter what.
    # --------------------------------------------------

    from app.utils.text_matching import resume_document_text

    resume_text = resume_document_text(resume)

    matched_keywords, missing_keywords = match_keywords(
        jd.keywords,
        resume_text
    )

    # --------------------------------------------------
    # Relevant experience / projects sourced from the
    # INVENTORY -- this is the "knowledge base" behavior:
    # surface things the candidate has done that are
    # relevant to this JD but may not be on the current
    # resume draft.
    # --------------------------------------------------

    jd_terms = (
        jd.required_skills
        + jd.preferred_skills
        + jd.keywords
    )

    relevant_experience = find_relevant_experience(
        inventory,
        jd_terms
    )

    relevant_projects = find_relevant_projects(
        inventory,
        jd_terms
    )

    # --------------------------------------------------
    # Summary opportunities: matched/inventory skills that
    # aren't mentioned anywhere in the summary yet.
    # --------------------------------------------------

    summary_text = " ".join(
        inventory.summary_points
        + inventory.summary_keywords
    ).lower()

    summary_opportunities = [
        skill
        for skill in (matched_skills + inventory_skill_matches)
        if skill not in summary_text
    ]

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

        relevant_experience=sorted(
            relevant_experience
        ),

        relevant_projects=sorted(
            relevant_projects
        ),

        summary_opportunities=sorted(
            set(summary_opportunities)
        )
    )

    logger.info(
        "gap_analysis=%s",
        result.model_dump()
    )

    return {
        "gap_analysis": result
    }
    
