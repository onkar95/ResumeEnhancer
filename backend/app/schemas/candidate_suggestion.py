from pydantic import BaseModel
from typing import List, Optional,Any


class Suggestion(BaseModel):

    suggestion_id: str

    section: str

    subsection: Optional[str] = None

    current_content: Optional[str] = None

    suggested_content: Any

    reason: str

    confidence: float

    requires_user_confirmation: bool = True

    status: str = "pending"

    user_rating: Optional[int] = None
    # used for skills

    user_edited_content: Optional[str] = None


class CandidateSuggestion(BaseModel):

    suggestions: List[
        Suggestion
    ] = []
