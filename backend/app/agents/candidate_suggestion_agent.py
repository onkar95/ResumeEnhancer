import re
from uuid import uuid4

from app.utils.skill_normalizer import normalize_skill
from app.workflows.state import (
    ResumeTailorState
)

from app.schemas.candidate_suggestion import (
    CandidateSuggestion,
    Suggestion
)


def _text_similarity(a: str, b: str) -> float:
    """
    Cheap word-overlap (Jaccard) similarity. Used to avoid suggesting
    "this content is missing" when it's really just a paraphrase of
    what's already on the resume -- an exact substring check flags
    almost every paraphrase as "missing", which is noisy and unhelpful
    for the human reviewing suggestions.
    """

    words_a = set(re.findall(r"[a-z0-9]+", a.lower()))
    words_b = set(re.findall(r"[a-z0-9]+", b.lower()))

    if not words_a or not words_b:
        return 0.0

    intersection = words_a & words_b
    union = words_a | words_b

    return len(intersection) / len(union)


def candidate_suggestion_node(
    state: ResumeTailorState
):
    """
    Surfaces suggestions the tailor step did NOT (or could not) apply on
    its own, for human review. Runs against the TAILORED resume (falling
    back to the original parsed resume if tailoring hasn't happened yet).
    """

    resume = state.get("tailored_resume") or state["parsed_resume"]
    inventory = state["resume_inventory"]
    jd = state["parsed_jd"]

    suggestions = []

    # Skills
    inventory_skills = {
        normalize_skill(skill.name)
        for skill in inventory.skills
    }
    resume_skills = {
        normalize_skill(skill)
        for category in resume.technical_skills.categories
        for skill in category.skills
    }
    jd_skills = jd.required_skills + jd.preferred_skills + jd.keywords

    for skill in set(jd_skills):
        normalized = normalize_skill(skill)
        if normalized in inventory_skills and normalized not in resume_skills:
            suggestions.append(
                Suggestion(
                    suggestion_id=str(uuid4()),
                    section="technical_skills",
                    subsection=None,
                    current_content=None,
                    suggested_content=skill,
                    reason="Found in inventory and relevant to JD but missing from resume.",
                    confidence=0.85
                )
            )

    # Certifications
    resume_certifications = {cert.name.lower()
                             for cert in resume.certifications}
    for cert in inventory.certifications:
        if cert.name.lower() not in resume_certifications:
            suggestions.append(
                Suggestion(
                    suggestion_id=str(uuid4()),
                    section="certifications",
                    subsection=None,
                    current_content=None,
                    suggested_content=cert.name,
                    reason="Certification exists in inventory but is not included in resume.",
                    confidence=0.80
                )
            )

    # Projects
    resume_project_titles = {
        project.title.lower()
        for exp in resume.professional_experience
        for project in exp.projects
    }
    for exp in inventory.professional_experience:
        for project in exp.projects:
            if project.title.lower() not in resume_project_titles:
                suggestions.append(
                    Suggestion(
                        suggestion_id=str(uuid4()),
                        section="professional_experience",
                        subsection=exp.company,
                        current_content=None,
                        suggested_content={
                            "title": project.title,
                            "bullet_points": project.bullet_points
                        },
                        reason=f"Project from {exp.company} is missing from resume.",
                        confidence=0.90
                    )
                )

    # Summary -- skip near-duplicate paraphrases (similarity >= 0.5) so a
    # differently-worded-but-equivalent summary doesn't generate noise.
    for summary in inventory.summary_points:
        similarity = _text_similarity(
            summary, resume.professional_summary.content)
        if similarity >= 0.5:
            continue
        if summary.lower() not in resume.professional_summary.content.lower():
            suggestions.append(
                Suggestion(
                    suggestion_id=str(uuid4()),
                    section="professional_summary",
                    subsection=None,
                    current_content=resume.professional_summary.content,
                    suggested_content=summary,
                    reason="Relevant summary content exists in inventory.",
                    confidence=0.70
                )
            )

    return {
        "candidate_suggestions": CandidateSuggestion(suggestions=suggestions)
    }
