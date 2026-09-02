
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

