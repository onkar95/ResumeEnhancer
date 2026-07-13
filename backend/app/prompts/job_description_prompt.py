
def build_job_description_prompt(jd_text: str) -> str:
    return f"""
You are an expert technical recruiter and ATS specialist.

Extract structured information from the job description.

IMPORTANT SKILL NORMALIZATION RULES:

1. Return skills in canonical industry-standard form.
2. Convert versions into the base technology.
3. Split combined skills into individual skills.
4. Remove duplicates.
5. Use lowercase.

Examples:

React JS -> react
React.js -> react
ReactJS -> react

NodeJS -> node.js
Node JS -> node.js

Java8 -> java
Java 17 -> java
Java21 -> java

SpringBoot -> spring boot
SpringBoot3 -> spring boot

Mongo DB -> mongodb

Postgres -> postgresql

AWS Lambda -> aws lambda

CI/CD -> ci/cd

JPA/Hibernate -> jpa, hibernate

Maven/Gradle -> maven, gradle

React JS/React Native -> react, react native

DO NOT RETURN:
- Versions
- Slash separated skills
- Combined skills

Return valid JSON only.

Schema:

{{
  "job_details": {{
    "title": "",
    "company": "",
    "location": "",
    "employment_type": ""
  }},
  "summary": "",
  "responsibilities": [],
  "required_skills": [],
  "preferred_skills": [],
  "qualifications": [],
  "keywords": [],
  "education_required": ""
}}

JOB DESCRIPTION:

{jd_text}
"""


# 
# from string import Template


# JOB_DESCRIPTION_PROMPT = Template(
#     """
# You are an expert ATS Job Description parser.

# Your task is to analyze the provided Job Description and extract structured information.

# IMPORTANT RULES:

# 1. Return ONLY valid JSON.
# 2. Do NOT wrap the response in markdown.
# 3. Do NOT include explanations.
# 4. Do NOT invent information.
# 5. If a value is missing, use null.
# 6. If a list section is missing, return an empty array.
# 7. Extract as much information as possible from the JD.

# Return JSON in the following format:

# {
#   "job_details": {
#     "title": null,
#     "company": null,
#     "location": null,
#     "employment_type": null,
#     "experience_required": null
#   },
#   "summary": null,
#   "responsibilities": [],
#   "required_skills": [],
#   "preferred_skills": [],
#   "qualifications": [],
#   "keywords": [],
#   "education_required": null
# }

# JOB DESCRIPTION:

# $job_description
# """
# )


# def build_job_description_prompt(
#     job_description: str
# ) -> str:
#     """
#     Build prompt for Job Description parsing.
#     """

#     return JOB_DESCRIPTION_PROMPT.substitute(
#         job_description=job_description
#     )