import re


CANONICAL_SKILLS = {

    "javascript (es6+)": "javascript",
    "javascript es6+": "javascript",
    "js": "javascript",

    "react.js": "react",
    "reactjs": "react",
    "react js": "react",

    "react-native": "react native",
    "reactnative": "react native",

    "redux toolkit": "redux",

    "nodejs": "node.js",
    "node js": "node.js",

    "express.js": "express",
    "expressjs": "express",

    "next.js": "next.js",
    "nextjs": "next.js",

    "springboot": "spring boot",
    "springboot3": "spring boot",
    "spring boot3": "spring boot",

    "postgres": "postgresql",
    "postgres sql": "postgresql",

    "mongo": "mongodb",
    "mongo db": "mongodb",

    "gitlab ci": "gitlab ci/cd",
    "gitlab cicd": "gitlab ci/cd",

    "rabbit mq": "rabbitmq",
    "active mq": "activemq",

    "typescript": "typescript",
    "ts": "typescript",

    "tailwind": "tailwind css",
    "tailwindcss": "tailwind css",
}


def normalize_skill(skill: str) -> str:
    if not skill:
        return ""

    skill = skill.strip().lower()

    # strip trailing version numbers, e.g. "java8" / "java 17" / "java21"
    skill = re.sub(r"\s*\d+(\.\d+)*\+?$", "", skill)

    skill = re.sub(r"\s+", " ", skill).strip()

    return CANONICAL_SKILLS.get(
        skill,
        skill
    )