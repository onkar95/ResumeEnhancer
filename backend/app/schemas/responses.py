"""
Common API Response Models

Reusable response models for all APIs.
"""

from typing import Any, Optional

from pydantic import BaseModel


from app.schemas.resume_inventory import (
    ResumeInventory
)


class InventoryResponse(
    BaseModel
):

    success: bool = True

    inventory: ResumeInventory


class SuggestionApprovalResponse(
    BaseModel
):

    success: bool = True

    approved_count: int


class APIResponse(BaseModel):
    """
    Standard API Response
    """

    success: bool = True

    message: str = ""

    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    """
    Standard Error Response
    """

    success: bool = False

    message: str

    error: Optional[str] = None
