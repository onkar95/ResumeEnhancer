from typing import Any, Dict


def normalize_jd(
    data: Dict[str, Any]
) -> Dict[str, Any]:

    if not isinstance(data, dict):
        return {}

    # --------------------------------------------------
    # JOB DETAILS
    # --------------------------------------------------

    if data.get("job_details") is None:
        data["job_details"] = {}

    # --------------------------------------------------
    # LIST FIELDS
    # --------------------------------------------------

    list_fields = [
        "responsibilities",
        "required_skills",
        "preferred_skills",
        "qualifications",
        "keywords",
    ]

    for field in list_fields:

        value = data.get(field)

        if value is None:
            data[field] = []

        elif not isinstance(value, list):
            data[field] = [str(value)]

    # --------------------------------------------------
    # STRING FIELDS
    # --------------------------------------------------

    string_fields = [
        "summary",
        "education_required",
    ]

    for field in string_fields:

        value = data.get(field)

        if value is not None:
            data[field] = str(value)

    # --------------------------------------------------
    # JOB DETAILS FIELDS
    # --------------------------------------------------

    job_details_fields = [
        "title",
        "company",
        "location",
        "employment_type",
        "experience_required",
    ]

    for field in job_details_fields:

        value = data["job_details"].get(field)

        if value is not None:
            data["job_details"][field] = str(value)

    return data