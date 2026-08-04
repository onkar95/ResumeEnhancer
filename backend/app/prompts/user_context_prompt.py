def build_user_context_prompt(user_instructions: str) -> str:
    return f"""
You are analyzing free-form notes a job candidate wrote for an AI
resume-tailoring tool.

The candidate may mention:

- Skills, technologies, or tools they have worked with that might not
  appear on their resume or their skill inventory, along with how
  confident/experienced they are with each.
- Preferences for how aggressively the tailored resume should incorporate
  job-description skills/keywords.

Extract structured JSON with this schema:

{{
  "declared_skills": [
    {{"skill": "", "confidence": 0.0, "note": ""}}
  ],
  "tailoring_mode": null
}}

Rules:

1. "declared_skills": Only include skills or technologies the candidate
   EXPLICITLY says they have used/worked with. Do NOT invent skills.

2. "confidence" is a 0.0-1.0 estimate of how strongly the candidate signals
   real hands-on experience (words like "extensively", "briefly", "a bit",
   "years", "one project" all shift this). Default to 0.6 if unclear but
   the candidate does state prior use.

3. "note": short (<12 words) restatement of context, e.g. "used briefly in
   a side project", or null if nothing extra was said.

4. "tailoring_mode": one of "aggressive", "strict", "balanced", or null if
   the candidate didn't express a preference.
   - "aggressive" = candidate wants as many JD-relevant skills/keywords
     woven in as can be reasonably justified.
   - "strict" = candidate wants ONLY resume/inventory content used, no
     embellishment.
   - "balanced" = default, moderate tailoring.

Return ONLY valid JSON. No markdown, no explanation, no code fences.

CANDIDATE NOTES:

{user_instructions}
"""