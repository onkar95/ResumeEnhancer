from pydantic import BaseModel
from typing import List


class SuggestionApprovalRequest(
    BaseModel
):

    run_id: str

    suggestion_ids: List[str]