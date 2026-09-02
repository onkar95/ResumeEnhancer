
from pydantic import BaseModel, Field
from typing import List


class TailoringContext(BaseModel):

    skills_to_add: List[str] = Field(
        default_factory=list
    )

    skills_to_emphasize: List[str] = Field(
        default_factory=list
    )

    keyword_targets: List[str] = Field(
        default_factory=list
    )