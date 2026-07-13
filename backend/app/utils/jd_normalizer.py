
import re
from typing import Any


def _clean_skill(skill: str) -> str:
    skill = skill.lower().strip()

    skill = re.sub(r"[()]", "", skill)
    skill = re.sub(r"\s+", " ", skill)

    return skill


def _clean_list(values: list[str]) -> list[str]:
    seen = set()
    result = []

    for value in values:
        value = _clean_skill(value)

        if value and value not in seen:
            seen.add(value)
            result.append(value)

    return result


def normalize_jd(data: dict[str, Any]) -> dict[str, Any]:
    data["required_skills"] = _clean_list(
        data.get("required_skills", [])
    )

    data["preferred_skills"] = _clean_list(
        data.get("preferred_skills", [])
    )

    data["keywords"] = _clean_list(
        data.get("keywords", [])
    )

    return data

# from typing import Any, Dict


# def normalize_jd(
#     data: Dict[str, Any]
# ) -> Dict[str, Any]:

#     if not isinstance(data, dict):
#         return {}

#     # --------------------------------------------------
#     # JOB DETAILS
#     # --------------------------------------------------

#     if data.get("job_details") is None:
#         data["job_details"] = {}

#     # --------------------------------------------------
#     # LIST FIELDS
#     # --------------------------------------------------

#     list_fields = [
#         "responsibilities",
#         "required_skills",
#         "preferred_skills",
#         "qualifications",
#         "keywords",
#     ]

#     for field in list_fields:

#         value = data.get(field)

#         if value is None:
#             data[field] = []

#         elif not isinstance(value, list):
#             data[field] = [str(value)]

#     # --------------------------------------------------
#     # STRING FIELDS
#     # --------------------------------------------------

#     string_fields = [
#         "summary",
#         "education_required",
#     ]

#     for field in string_fields:

#         value = data.get(field)

#         if value is not None:
#             data[field] = str(value)

#     # --------------------------------------------------
#     # JOB DETAILS FIELDS
#     # --------------------------------------------------

#     job_details_fields = [
#         "title",
#         "company",
#         "location",
#         "employment_type",
#         "experience_required",
#     ]

#     for field in job_details_fields:

#         value = data["job_details"].get(field)

#         if value is not None:
#             data["job_details"][field] = str(value)

#     return data

