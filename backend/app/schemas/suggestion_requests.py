from pydantic import BaseModel
from typing import List

# schemas/suggestion_requests.py or a new file


class RunHistoryQuery(BaseModel):
    limit: int = 20
    offset: int = 0

class SuggestionApprovalRequest(
    BaseModel
):

    run_id: str

    suggestion_ids: List[str]
