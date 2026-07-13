import re


CANONICAL_SKILLS = {

    "javascript (es6+)": "javascript",

    "react.js": "react",
    "reactjs": "react",
    "react js": "react",

    "redux toolkit": "redux",

    "nodejs": "node.js",
    "node js": "node.js",

    "express.js": "express",

    "springboot": "spring boot",
    "springboot3": "spring boot",

    "postgres": "postgresql",
}


def normalize_skill(skill: str) -> str:
    if not skill:
        return ""

    skill = skill.strip().lower()

    skill = re.sub(r"\s+", " ", skill)

    return CANONICAL_SKILLS.get(
        skill,
        skill
    )