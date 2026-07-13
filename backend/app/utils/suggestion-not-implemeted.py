# """
# Job Description Normalizer

# Converts raw LLM output into a consistent format used
# throughout the workflow.

# Responsibilities

# - Normalize skill names
# - Split grouped skills
# - Remove duplicates
# - Generate searchable keywords
# """

# import re
# from copy import deepcopy


# # ---------------------------------------------------------
# # Skill aliases
# # ---------------------------------------------------------

# SKILL_ALIASES = {
#     # Languages
#     "java8": "java",
#     "java 8": "java",
#     "java17": "java",
#     "java 17": "java",
#     "java21": "java",
#     "java 21": "java",
#     "java8/17/21": "java",

#     "javascript es6+": "javascript",
#     "javascript (es6+)": "javascript",
#     "js": "javascript",

#     # React
#     "reactjs": "react",
#     "react js": "react",
#     "react.js": "react",

#     "reactnative": "react native",
#     "react-native": "react native",

#     # Spring
#     "springboot": "spring boot",
#     "spring boot3": "spring boot",
#     "springboot3": "spring boot",
#     "spring boot 3": "spring boot",

#     "spring security": "spring security",

#     # Node
#     "nodejs": "node.js",
#     "node js": "node.js",

#     # DB
#     "postgres": "postgresql",
#     "postgres sql": "postgresql",
#     "mongo": "mongodb",

#     # CI/CD
#     "gitlab ci": "gitlab ci/cd",
#     "gitlab ci cd": "gitlab ci/cd",

#     # MQ
#     "activemq": "active mq",
#     "rabbit mq": "rabbitmq",
# }


# # ---------------------------------------------------------
# # Words that shouldn't become keywords
# # ---------------------------------------------------------

# STOP_WORDS = {
#     "and",
#     "or",
#     "with",
#     "using",
#     "knowledge",
#     "experience",
#     "skills",
#     "ability",
#     "working",
#     "good",
#     "excellent",
#     "strong",
#     "preferred",
#     "required",
# }


# # ---------------------------------------------------------
# # Compound phrases we want to split
# # ---------------------------------------------------------

# SPECIAL_SPLITS = {
#     "jpa/hibernate": [
#         "jpa",
#         "hibernate",
#     ],
#     "maven/gradle": [
#         "maven",
#         "gradle",
#     ],
#     "postgresql/mysql": [
#         "postgresql",
#         "mysql",
#     ],
#     "react js/react native": [
#         "react",
#         "react native",
#     ],
#     "react js / react native": [
#         "react",
#         "react native",
#     ],
#     "java8/17/21": [
#         "java",
#     ],
# }


# # ---------------------------------------------------------
# # Helpers
# # ---------------------------------------------------------

# def normalize_skill(skill: str) -> str:

#     skill = skill.lower().strip()

#     skill = re.sub(r"\(.*?\)", "", skill)

#     skill = skill.replace("&", " and ")

#     skill = re.sub(r"\s+", " ", skill)

#     skill = skill.strip()

#     if skill in SPECIAL_SPLITS:
#         return skill

#     return SKILL_ALIASES.get(skill, skill)


# def split_skill(skill: str):

#     skill = skill.lower().strip()

#     if skill in SPECIAL_SPLITS:
#         return SPECIAL_SPLITS[skill]

#     separators = [
#         ",",
#         ";",
#         "|",
#     ]

#     result = [skill]

#     for sep in separators:

#         new = []

#         for item in result:

#             new.extend(item.split(sep))

#         result = new

#     final = []

#     for item in result:

#         item = item.strip()

#         if not item:
#             continue

#         final.append(
#             normalize_skill(item)
#         )

#     return final


# def deduplicate(values):

#     seen = set()

#     output = []

#     for value in values:

#         value = value.strip()

#         if not value:
#             continue

#         if value in seen:
#             continue

#         seen.add(value)

#         output.append(value)

#     return output


# # ---------------------------------------------------------
# # Main
# # ---------------------------------------------------------

# def normalize_jd(data: dict) -> dict:

#     jd = deepcopy(data)

#     required = []

#     preferred = []

#     keywords = []

#     # ---------------- Required ----------------

#     for skill in jd.get("required_skills", []):

#         required.extend(
#             split_skill(skill)
#         )

#     # ---------------- Preferred ----------------

#     for skill in jd.get("preferred_skills", []):

#         preferred.extend(
#             split_skill(skill)
#         )

#     required = deduplicate(required)

#     preferred = deduplicate(preferred)

#     # ---------------- Keywords ----------------

#     for skill in required + preferred:

#         if skill not in keywords:
#             keywords.append(skill)

#     for responsibility in jd.get("responsibilities", []):

#         words = re.findall(
#             r"[A-Za-z0-9.+#/]+",
#             responsibility.lower(),
#         )

#         for word in words:

#             if len(word) < 3:
#                 continue

#             if word in STOP_WORDS:
#                 continue

#             if word not in keywords:
#                 keywords.append(word)

#     jd["required_skills"] = required
#     jd["preferred_skills"] = preferred
#     jd["keywords"] = deduplicate(keywords)

#     return jd