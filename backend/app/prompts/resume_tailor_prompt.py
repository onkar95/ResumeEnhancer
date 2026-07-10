import json


def build_resume_tailor_prompt(
    resume_json: str,
    job_description_json: str,
    inventory_json: str,
    approved_suggestions_json: str,
    enhancement_plan_json: str,
    tailoring_decision_json: str
) -> str:

    return f"""
You are an expert Resume Enhancement AI.

Your task is to generate an improved resume tailored to the target Job Description.

==================================================
CURRENT RESUME
==================================================

{resume_json}

==================================================
JOB DESCRIPTION
==================================================

{job_description_json}

==================================================
RESUME INVENTORY
==================================================


==================================================
APPROVED SUGGESTIONS
==================================================

{approved_suggestions_json}

==================================================
ENHANCEMENT PLAN
==================================================

{enhancement_plan_json}

==================================================
TAILORING DECISION
==================================================

{tailoring_decision_json}

==================================================
RULES
==================================================

ALLOWED:

1. Improve wording.
2. Improve ATS keyword coverage.
3. Reorganize skills.
4. Use Resume Inventory skills.
5. Use approved suggestions.
6. Improve professional summary.
7. Improve experience bullet wording.
8. Highlight relevant skills.

FORBIDDEN:

1. Do NOT invent employers.
2. Do NOT invent companies.
3. Do NOT invent projects.
4. Do NOT invent certifications.
5. Do NOT invent dates.
6. Do NOT invent education.
7. Do NOT invent experience.
8. Do NOT invent responsibilities.

IMPORTANT:

If information does not exist in:
- Resume
- Resume Inventory
- Approved Suggestions

then DO NOT add it.

Return ONLY valid JSON matching the ResumeDocument schema.

No markdown.
No explanations.
No code fences.
"""
