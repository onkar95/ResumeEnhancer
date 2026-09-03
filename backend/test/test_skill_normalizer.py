# backend/tests/test_skill_normalizer.py
from app.utils.skill_normalizer import normalize_skill

def test_normalizes_js_variants():
    assert normalize_skill("ReactJS") == "react"
    assert normalize_skill("React.js") == "react"
    assert normalize_skill("Node JS") == "node.js"

def test_strips_version_numbers():
    assert normalize_skill("java 17") == "java"
    assert normalize_skill("java21") == "java"

# backend/tests/test_gap_analysis.py
from app.agents.gap_analysis_agent import extract_resume_skills
# build a minimal ResumeDocument fixture, assert extract_resume_skills(...) output

# backend/tests/test_workflow_smoke.py
# ainvoke resume_tailor_graph with a fixture PDF + short JD text,
# assert result["comparison_data"].ats_after >= result["comparison_data"].ats_before