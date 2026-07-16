from pydantic import BaseModel, Field
from typing import List


class EnhancementPlan(BaseModel):

    skills_to_add: List[str] = []

    skills_to_emphasize: List[str] = []

    experience_to_emphasize: List[str] = []

    projects_to_emphasize: List[str] = []

    keyword_targets: List[str] = []

    summary_improvements: List[str] = Field( default_factory=list)

