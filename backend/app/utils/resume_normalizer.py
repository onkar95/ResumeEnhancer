
"""
Resume Normalizer

Converts raw LLM output into a ResumeDocument-compatible dictionary.

This layer performs ONLY structural normalization.

It does NOT rewrite resume content.

Author: Resume Tailor AI
"""

from copy import deepcopy


def normalize_resume(
    data: dict,
) -> dict:
    """
    Normalize parsed resume dictionary.

    Handles:

    - missing objects
    - missing arrays
    - string -> object conversion
    - dict -> list conversion

    Returns

    Normalized dictionary.
    """

    if not isinstance(data, dict):
        raise ValueError(
            "Resume parser returned invalid data."
        )

    normalized = deepcopy(data)

    # -----------------------------------------------------
    # Required Objects
    # -----------------------------------------------------

    normalized.setdefault(
        "contact_info",
        {},
    )

    normalized.setdefault(
        "professional_summary",
        {
            "content": ""
        },
    )

    normalized.setdefault(
        "technical_skills",
        {
            "categories": []
        },
    )

    normalized.setdefault(
        "layout_hints",
        {},
    )

    # -----------------------------------------------------
    # Required Lists
    # -----------------------------------------------------

    normalized.setdefault(
        "professional_experience",
        [],
    )

    normalized.setdefault(
        "education",
        [],
    )

    normalized.setdefault(
        "certifications",
        [],
    )

    # -----------------------------------------------------
    # Education
    # dict -> list
    # -----------------------------------------------------

    if isinstance(
        normalized["education"],
        dict,
    ):
        normalized["education"] = [
            normalized["education"]
        ]

    # -----------------------------------------------------
    # Experience
    # dict -> list
    # -----------------------------------------------------

    if isinstance(
        normalized["professional_experience"],
        dict,
    ):
        normalized[
            "professional_experience"
        ] = [
            normalized[
                "professional_experience"
            ]
        ]

    # -----------------------------------------------------
    # Certifications
    # string -> object
    # -----------------------------------------------------

    certifications = []

    for cert in normalized["certifications"]:

        if isinstance(cert, str):

            certifications.append(
                {
                    "name": cert
                }
            )

        else:

            certifications.append(cert)

    normalized[
        "certifications"
    ] = certifications

    # -----------------------------------------------------
    # Experience Projects
    # -----------------------------------------------------

    for exp in normalized[
        "professional_experience"
    ]:

        exp.setdefault(
            "responsibilities",
            [],
        )

        exp.setdefault(
            "projects",
            [],
        )

        projects = []

        for project in exp["projects"]:

            if isinstance(project, str):

                projects.append(
                    {
                        "title": project,
                        "bullet_points": [],
                        "technologies": [],
                    }
                )

            else:

                project.setdefault(
                    "bullet_points",
                    [],
                )

                # Accept a plain string too, in case the LLM writes
                # "technologies": "React, Node.js" instead of a list.
                technologies = project.get("technologies", [])

                if isinstance(technologies, str):
                    technologies = [
                        t.strip()
                        for t in technologies.split(",")
                        if t.strip()
                    ]

                project["technologies"] = technologies or []

                projects.append(project)

        exp["projects"] = projects

    return normalized

# """
# Resume Normalizer

# Converts raw LLM output into a ResumeDocument-compatible dictionary.

# This layer performs ONLY structural normalization.

# It does NOT rewrite resume content.

# Author: Resume Tailor AI
# """

# from copy import deepcopy


# def normalize_resume(
#     data: dict,
# ) -> dict:
#     """
#     Normalize parsed resume dictionary.

#     Handles:

#     - missing objects
#     - missing arrays
#     - string -> object conversion
#     - dict -> list conversion

#     Returns

#     Normalized dictionary.
#     """

#     if not isinstance(data, dict):
#         raise ValueError(
#             "Resume parser returned invalid data."
#         )

#     normalized = deepcopy(data)

#     # -----------------------------------------------------
#     # Required Objects
#     # -----------------------------------------------------

#     normalized.setdefault(
#         "contact_info",
#         {},
#     )

#     normalized.setdefault(
#         "professional_summary",
#         {
#             "content": ""
#         },
#     )

#     normalized.setdefault(
#         "technical_skills",
#         {
#             "categories": []
#         },
#     )

#     normalized.setdefault(
#         "layout_hints",
#         {},
#     )

#     # -----------------------------------------------------
#     # Required Lists
#     # -----------------------------------------------------

#     normalized.setdefault(
#         "professional_experience",
#         [],
#     )

#     normalized.setdefault(
#         "education",
#         [],
#     )

#     normalized.setdefault(
#         "certifications",
#         [],
#     )

#     # -----------------------------------------------------
#     # Education
#     # dict -> list
#     # -----------------------------------------------------

#     if isinstance(
#         normalized["education"],
#         dict,
#     ):
#         normalized["education"] = [
#             normalized["education"]
#         ]

#     # -----------------------------------------------------
#     # Experience
#     # dict -> list
#     # -----------------------------------------------------

#     if isinstance(
#         normalized["professional_experience"],
#         dict,
#     ):
#         normalized[
#             "professional_experience"
#         ] = [
#             normalized[
#                 "professional_experience"
#             ]
#         ]

#     # -----------------------------------------------------
#     # Certifications
#     # string -> object
#     # -----------------------------------------------------

#     certifications = []

#     for cert in normalized["certifications"]:

#         if isinstance(cert, str):

#             certifications.append(
#                 {
#                     "name": cert
#                 }
#             )

#         else:

#             certifications.append(cert)

#     normalized[
#         "certifications"
#     ] = certifications

#     # -----------------------------------------------------
#     # Experience Projects
#     # -----------------------------------------------------

#     for exp in normalized[
#         "professional_experience"
#     ]:

#         exp.setdefault(
#             "responsibilities",
#             [],
#         )

#         exp.setdefault(
#             "projects",
#             [],
#         )

#         projects = []

#         for project in exp["projects"]:

#             if isinstance(project, str):

#                 projects.append(
#                     {
#                         "title": project,
#                         "bullet_points": [],
#                     }
#                 )

#             else:

#                 project.setdefault(
#                     "bullet_points",
#                     [],
#                 )

#                 projects.append(project)

#         exp["projects"] = projects

#     return normalized