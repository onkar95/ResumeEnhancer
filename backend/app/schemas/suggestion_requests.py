from pydantic import BaseModel
from typing import List


class SuggestionApprovalRequest(
    BaseModel
):

    suggestion_ids: List[str]