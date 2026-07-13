# from pydantic import BaseModel, Field
# from typing import List


# class TailoringContext(BaseModel):

#     current_resume_skills: List[
#         str
#     ] = Field(default_factory=list)

#     inventory_skills: List[
#         str
#     ] = Field(default_factory=list)

#     approved_skills: List[
#         str
#     ] = Field(default_factory=list)

#     skills_to_add: List[
#         str
#     ] = Field(default_factory=list)

#     skills_to_emphasize: List[
#         str
#     ] = Field(default_factory=list)

#     keyword_targets: List[
#         str
#     ] = Field(default_factory=list)

#     inferred_skills: List[
#         str
#     ] = Field(default_factory=list)

#     inferred_experience: List[
#         str
#     ] = Field(default_factory=list)

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