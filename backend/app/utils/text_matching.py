"""
Shared text search utilities.

This replaces three slightly-different, inconsistent keyword-matching
implementations that used to live separately in gap_analysis_agent,
validation_agent, and comparison_agent. All three now import from here
so "is this keyword present" means the same thing everywhere.

Key idea: skills (from technical_skills / InventorySkill lists) should be
matched as normalized tokens (exact set membership). Free-text JD keywords
("deployment pipelines", "operational excellence") are NOT skill tokens and
will never appear in a skills list -- they must be searched across the full
resume text (summary + experience + project bullets), the same way a human
recruiter or an ATS text-scanner would.
"""

import re
from typing import Iterable, List, Tuple


def _experience_text(experiences) -> List[str]:
    """
    Works for both ResumeDocument.professional_experience and
    ResumeInventory.professional_experience since both use the same
    ExperienceEntry / ExperienceProject schema.
    """
    chunks: List[str] = []

    for exp in experiences or []:
        if getattr(exp, "role", None):
            chunks.append(exp.role)
        if getattr(exp, "company", None):
            chunks.append(exp.company)

        chunks.extend(exp.responsibilities or [])

        for project in getattr(exp, "projects", []) or []:
            if project.title:
                chunks.append(project.title)
            chunks.extend(project.bullet_points or [])
            chunks.extend(getattr(project, "technologies", None) or [])

    return chunks


def resume_document_text(resume) -> str:
    """Full lowercase searchable text for a ResumeDocument (the draft/base resume)."""
    chunks: List[str] = []

    if resume.headline:
        chunks.append(resume.headline)

    if resume.professional_summary and resume.professional_summary.content:
        chunks.append(resume.professional_summary.content)

    for category in resume.technical_skills.categories:
        chunks.extend(category.skills)

    chunks.extend(_experience_text(resume.professional_experience))

    for cert in resume.certifications:
        chunks.append(cert.name)

    for edu in resume.education:
        chunks.append(edu.degree)
        chunks.append(edu.institution)

    return " ".join(str(c) for c in chunks if c).lower()


def resume_inventory_text(inventory) -> str:
    """
    Full lowercase searchable text for a ResumeInventory -- i.e. the
    candidate's whole knowledge base, not just what's on the current resume.
    """
    chunks: List[str] = []

    chunks.extend(inventory.summary_points or [])
    chunks.extend(skill.name for skill in inventory.skills)
    chunks.extend(_experience_text(inventory.professional_experience))

    for cert in inventory.certifications:
        chunks.append(cert.name)

    for edu in inventory.education:
        chunks.append(edu.degree)
        chunks.append(edu.institution)

    return " ".join(str(c) for c in chunks if c).lower()


def keyword_in_text(keyword: str, text: str) -> bool:
    """
    Substring match with light word-boundary protection so short keywords
    (e.g. 'ci', 'go') don't false-positive inside unrelated words.
    Multi-word / slash-containing keywords are matched as plain substrings.
    """
    keyword = (keyword or "").strip().lower()

    if not keyword:
        return False

    if len(keyword) <= 3 or " " in keyword or "/" in keyword:
        return keyword in text

    pattern = r"(?<![a-z0-9])" + re.escape(keyword) + r"(?![a-z0-9])"
    return re.search(pattern, text) is not None


def match_keywords(
    keywords: Iterable[str],
    text: str,
) -> Tuple[List[str], List[str]]:
    """Returns (matched, missing) preserving input order, deduped."""
    matched: List[str] = []
    missing: List[str] = []
    seen = set()

    for kw in keywords:
        key = (kw or "").strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)

        if keyword_in_text(kw, text):
            matched.append(kw)
        else:
            missing.append(kw)

    return matched, missing



# """
# Shared text search utilities.

# This replaces three slightly-different, inconsistent keyword-matching
# implementations that used to live separately in gap_analysis_agent,
# validation_agent, and comparison_agent. All three now import from here
# so "is this keyword present" means the same thing everywhere.

# Key idea: skills (from technical_skills / InventorySkill lists) should be
# matched as normalized tokens (exact set membership). Free-text JD keywords
# ("deployment pipelines", "operational excellence") are NOT skill tokens and
# will never appear in a skills list -- they must be searched across the full
# resume text (summary + experience + project bullets), the same way a human
# recruiter or an ATS text-scanner would.
# """

# import re
# from typing import Iterable, List, Tuple


# def _experience_text(experiences) -> List[str]:
#     """
#     Works for both ResumeDocument.professional_experience and
#     ResumeInventory.professional_experience since both use the same
#     ExperienceEntry / ExperienceProject schema.
#     """
#     chunks: List[str] = []

#     for exp in experiences or []:
#         if getattr(exp, "role", None):
#             chunks.append(exp.role)
#         if getattr(exp, "company", None):
#             chunks.append(exp.company)

#         chunks.extend(exp.responsibilities or [])

#         for project in getattr(exp, "projects", []) or []:
#             if project.title:
#                 chunks.append(project.title)
#             chunks.extend(project.bullet_points or [])

#     return chunks


# def resume_document_text(resume) -> str:
#     """Full lowercase searchable text for a ResumeDocument (the draft/base resume)."""
#     chunks: List[str] = []

#     if resume.headline:
#         chunks.append(resume.headline)

#     if resume.professional_summary and resume.professional_summary.content:
#         chunks.append(resume.professional_summary.content)

#     for category in resume.technical_skills.categories:
#         chunks.extend(category.skills)

#     chunks.extend(_experience_text(resume.professional_experience))

#     for cert in resume.certifications:
#         chunks.append(cert.name)

#     for edu in resume.education:
#         chunks.append(edu.degree)
#         chunks.append(edu.institution)

#     return " ".join(str(c) for c in chunks if c).lower()


# def resume_inventory_text(inventory) -> str:
#     """
#     Full lowercase searchable text for a ResumeInventory -- i.e. the
#     candidate's whole knowledge base, not just what's on the current resume.
#     """
#     chunks: List[str] = []

#     chunks.extend(inventory.summary_points or [])
#     chunks.extend(skill.name for skill in inventory.skills)
#     chunks.extend(_experience_text(inventory.professional_experience))

#     for cert in inventory.certifications:
#         chunks.append(cert.name)

#     for edu in inventory.education:
#         chunks.append(edu.degree)
#         chunks.append(edu.institution)

#     return " ".join(str(c) for c in chunks if c).lower()


# def keyword_in_text(keyword: str, text: str) -> bool:
#     """
#     Substring match with light word-boundary protection so short keywords
#     (e.g. 'ci', 'go') don't false-positive inside unrelated words.
#     Multi-word / slash-containing keywords are matched as plain substrings.
#     """
#     keyword = (keyword or "").strip().lower()

#     if not keyword:
#         return False

#     if len(keyword) <= 3 or " " in keyword or "/" in keyword:
#         return keyword in text

#     pattern = r"(?<![a-z0-9])" + re.escape(keyword) + r"(?![a-z0-9])"
#     return re.search(pattern, text) is not None


# def match_keywords(
#     keywords: Iterable[str],
#     text: str,
# ) -> Tuple[List[str], List[str]]:
#     """Returns (matched, missing) preserving input order, deduped."""
#     matched: List[str] = []
#     missing: List[str] = []
#     seen = set()

#     for kw in keywords:
#         key = (kw or "").strip().lower()
#         if not key or key in seen:
#             continue
#         seen.add(key)

#         if keyword_in_text(kw, text):
#             matched.append(kw)
#         else:
#             missing.append(kw)

#     return matched, missing