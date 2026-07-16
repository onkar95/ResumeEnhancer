import re

from app.schemas.resume import (
    ResumeDocument
)


STOP_WORDS = {
    "the",
    "and",
    "with",
    "for",
    "from",
    "into",
    "using",
    "used",
    "built",
    "developed",
    "implemented",
    "application",
    "applications",
    "system",
    "systems"
}


def extract_keywords(
    texts: list[str]
) -> list[str]:

    keywords = set()

    for text in texts:

        if not text:
            continue

        words = re.findall(
            r"[A-Za-z0-9+#.-]+",
            text.lower()
        )

        for word in words:

            if (
                len(word) < 3
                or word in STOP_WORDS
            ):
                continue

            keywords.add(word)

    return sorted(keywords)


def extract_resume_skills(
    resume: ResumeDocument
):

    skills = set()

    if not resume:
        return skills

    if not resume.technical_skills:
        return skills

    for category in (
        resume.technical_skills.categories
    ):

        for skill in category.skills:

            if skill:

                skills.add(
                    skill.strip().lower()
                )

    return skills


def experience_exists(
    company: str,
    role: str,
    experiences
):

    for exp in experiences:

        if (
            exp.company.lower()
            == company.lower()
            and
            exp.role.lower()
            == role.lower()
        ):
            return True

    return False