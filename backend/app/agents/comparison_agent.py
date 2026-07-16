from app.utils.skill_normalizer import (
    normalize_skill
)

from app.workflows.state import (
    ResumeTailorState
)

from app.schemas.comparison_result import (
    ComparisonResult
)


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


def extract_jd_targets(
    jd
):

    targets = set()

    for skill in (
        jd.required_skills
        + jd.preferred_skills
    ):

        targets.add(
            normalize_skill(skill)
        )

    for keyword in jd.keywords:

        targets.add(
            normalize_skill(keyword)
        )

    return targets


def calculate_ats(
    resume_skills,
    jd_targets
):

    if not jd_targets:
        return 0

    matched = len(
        resume_skills.intersection(
            jd_targets
        )
    )

    return round(
        (
            matched
            / len(jd_targets)
        )
        * 100
    )


def count_changed_experiences(
    original_resume,
    tailored_resume
):

    changed = 0

    original_entries = {
        (
            exp.company,
            exp.role
        ): exp
        for exp in original_resume.professional_experience
    }

    for tailored_exp in (
        tailored_resume.professional_experience
    ):

        key = (
            tailored_exp.company,
            tailored_exp.role
        )

        original_exp = (
            original_entries.get(key)
        )

        if not original_exp:
            continue

        if (
            original_exp.responsibilities
            != tailored_exp.responsibilities
        ):
            changed += 1

    return changed


def comparison_node(
    state: ResumeTailorState
):

    original_resume = state[
        "parsed_resume"
    ]

    tailored_resume = state[
        "tailored_resume"
    ]

    jd = state[
        "parsed_jd"
    ]

    gap_analysis = state.get(
        "gap_analysis"
    )

    enhancement_plan = state.get(
        "enhancement_plan"
    )

    original_skills = (
        extract_resume_skills(
            original_resume
        )
    )

    tailored_skills = (
        extract_resume_skills(
            tailored_resume
        )
    )

    jd_targets = (
        extract_jd_targets(
            jd
        )
    )

    ats_before = calculate_ats(
        original_skills,
        jd_targets
    )

    ats_after = calculate_ats(
        tailored_skills,
        jd_targets
    )

    added_skills = sorted(
        list(
            tailored_skills
            - original_skills
        )
    )

    comparison = ComparisonResult(

        inventory_skills_used=gap_analysis.inventory_skills
        if gap_analysis
        else [],

        approved_skills_added=added_skills,

        emphasized_skills=enhancement_plan.skills_to_emphasize
        if enhancement_plan
        else [],

        targeted_keywords=enhancement_plan.keyword_targets
        if enhancement_plan
        else [],

        summary_updated=(
            original_resume
            .professional_summary
            .content
            !=
            tailored_resume
            .professional_summary
            .content
        ),

        experience_sections_updated=count_changed_experiences(
            original_resume,
            tailored_resume
        ),

        ats_before=ats_before,

        ats_after=ats_after
    )

    return {
        "comparison_data":
            comparison
    }

# from app.agents.helpers import (
#     extract_resume_skills
# )

# from app.schemas.resume import (
#     ResumeDocument
# )

# from app.schemas.job_description import (
#     JobDescription
# )


# def normalize(values):

#     return {
#         str(v).strip().lower()
#         for v in values
#         if v
#     }


# def extract_jd_targets(
#     jd: JobDescription
# ):

#     required = normalize(
#         jd.required_skills
#     )

#     preferred = normalize(
#         jd.preferred_skills
#     )

#     keywords = normalize(
#         jd.keywords
#     )

#     return (
#         required
#         | preferred
#         | keywords
#     )


# def calculate_ats_score(
#     resume_skills,
#     jd_targets
# ):

#     if not jd_targets:
#         return 0

#     matched = len(
#         resume_skills.intersection(
#             jd_targets
#         )
#     )

#     return round(
#         (
#             matched
#             / len(jd_targets)
#         )
#         * 100
#     )


# def compare_summary(
#     original: ResumeDocument,
#     tailored: ResumeDocument
# ):

#     return {
#         "changed": (
#             original.professional_summary.content
#             != tailored.professional_summary.content
#         ),
#         "before": (
#             original.professional_summary.content
#         ),
#         "after": (
#             tailored.professional_summary.content
#         )
#     }


# def compare_experience(
#     original: ResumeDocument,
#     tailored: ResumeDocument
# ):

#     changes = []

#     original_entries = {
#         (
#             exp.company,
#             exp.role
#         ): exp
#         for exp in original.professional_experience
#     }

#     for tailored_exp in (
#         tailored.professional_experience
#     ):

#         key = (
#             tailored_exp.company,
#             tailored_exp.role
#         )

#         original_exp = (
#             original_entries.get(key)
#         )

#         if not original_exp:
#             continue

#         original_bullets = set(
#             original_exp.responsibilities
#         )

#         tailored_bullets = set(
#             tailored_exp.responsibilities
#         )

#         added_bullets = list(
#             tailored_bullets
#             - original_bullets
#         )

#         if added_bullets:

#             changes.append(
#                 {
#                     "company":
#                         tailored_exp.company,

#                     "role":
#                         tailored_exp.role,

#                     "added_bullets":
#                         added_bullets
#                 }
#             )

#     return changes


# async def comparison_node(state):

#     original_resume: ResumeDocument = (
#         state["parsed_resume"]
#     )

#     tailored_resume: ResumeDocument = (
#         state["tailored_resume"]
#     )

#     jd: JobDescription = (
#         state["parsed_jd"]
#     )

#     original_skills = (
#         extract_resume_skills(
#             original_resume
#         )
#     )

#     tailored_skills = (
#         extract_resume_skills(
#             tailored_resume
#         )
#     )

#     jd_targets = (
#         extract_jd_targets(jd)
#     )

#     added_skills = list(
#         tailored_skills
#         - original_skills
#     )

#     removed_skills = list(
#         original_skills
#         - tailored_skills
#     )

#     ats_before = calculate_ats_score(
#         original_skills,
#         jd_targets
#     )

#     ats_after = calculate_ats_score(
#         tailored_skills,
#         jd_targets
#     )

#     summary_changes = (
#         compare_summary(
#             original_resume,
#             tailored_resume
#         )
#     )

#     experience_changes = (
#         compare_experience(
#             original_resume,
#             tailored_resume
#         )
#     )

#     return {
#         "comparison_data": {

#             "ats_before":
#                 ats_before,

#             "ats_after":
#                 ats_after,

#             "added_skills":
#                 added_skills,

#             "removed_skills":
#                 removed_skills,

#             "summary_changes":
#                 summary_changes,

#             "experience_changes":
#                 experience_changes
#         }
#     }

print('hello')
#
# from app.agents.helpers import (
#     extract_resume_skills
# )


# def calculate_ats_score(
#     resume_skills,
#     jd_targets
# ):

#     if not jd_targets:
#         return 0

#     matched = len(
#         resume_skills.intersection(
#             jd_targets
#         )
#     )

#     return round(
#         (matched / len(jd_targets))
#         * 100
#     )


# async def comparison_node(state):

#     original_resume = (
#         state["parsed_resume"]
#     )

#     tailored_resume = (
#         state["tailored_resume"]
#     )

#     jd = state["parsed_jd"]

#     original_skills = (
#         extract_resume_skills(
#             original_resume
#         )
#     )

#     tailored_skills = (
#         extract_resume_skills(
#             tailored_resume
#         )
#     )

#     jd_targets = {
#         *[
#             x.lower()
#             for x in jd.get(
#                 "required_skills",
#                 []
#             )
#         ],
#         *[
#             x.lower()
#             for x in jd.get(
#                 "preferred_skills",
#                 []
#             )
#         ],
#         *[
#             x.lower()
#             for x in jd.get(
#                 "keywords",
#                 []
#             )
#         ]
#     }

#     added_skills = list(
#         tailored_skills
#         - original_skills
#     )

#     ats_before = calculate_ats_score(
#         original_skills,
#         jd_targets
#     )

#     ats_after = calculate_ats_score(
#         tailored_skills,
#         jd_targets
#     )

#     return {
#         "comparison_data": {
#             "added_skills": added_skills,
#             "ats_before": ats_before,
#             "ats_after": ats_after
#         }
#     }
