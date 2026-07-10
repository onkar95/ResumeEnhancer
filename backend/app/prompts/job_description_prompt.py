from string import Template


JOB_DESCRIPTION_PROMPT = Template(
    """
You are an expert ATS Job Description parser.

Your task is to analyze the provided Job Description and extract structured information.

IMPORTANT RULES:

1. Return ONLY valid JSON.
2. Do NOT wrap the response in markdown.
3. Do NOT include explanations.
4. Do NOT invent information.
5. If a value is missing, use null.
6. If a list section is missing, return an empty array.
7. Extract as much information as possible from the JD.

Return JSON in the following format:

{
  "job_details": {
    "title": null,
    "company": null,
    "location": null,
    "employment_type": null,
    "experience_required": null
  },
  "summary": null,
  "responsibilities": [],
  "required_skills": [],
  "preferred_skills": [],
  "qualifications": [],
  "keywords": [],
  "education_required": null
}

JOB DESCRIPTION:

$job_description
"""
)


def build_job_description_prompt(
    job_description: str
) -> str:
    """
    Build prompt for Job Description parsing.
    """

    return JOB_DESCRIPTION_PROMPT.substitute(
        job_description=job_description
    )