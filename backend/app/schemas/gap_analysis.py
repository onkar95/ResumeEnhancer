from pydantic import BaseModel
from typing import List


class GapAnalysis(BaseModel):

    matched_skills: List[str] = []

    inventory_skills: List[str] = []

    missing_skills: List[str] = []

    matched_keywords: List[str] = []

    missing_keywords: List[str] = []

    relevant_experience: List[str] = []

    relevant_projects: List[str] = []
    
    summary_opportunities: List[str] = []
