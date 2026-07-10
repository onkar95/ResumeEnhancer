from app.schemas.resume import (
    ResumeDocument
)


def extract_resume_skills(
    resume: ResumeDocument
):

    skills = set()

    if not resume:
        return skills

    if not resume.technical_skills:
        return skills

    for category in resume.technical_skills.categories:

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

# def extract_resume_skills(
#     resume: dict
# ) -> Set[str]:

#     skills = set()

#     technical_skills = (
#         resume.get("technical_skills", {})
#     )

#     categories = technical_skills.get(
#         "categories",
#         []
#     )

#     for category in categories:

#         for skill in category.get(
#             "skills",
#             []
#         ):

#             skills.add(
#                 skill.strip().lower()
#             )

#     return skills
