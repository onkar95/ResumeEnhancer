
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

