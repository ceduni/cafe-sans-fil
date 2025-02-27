"""
Module for global models.
"""

from typing import List, Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class Id:
    """Model for generic ID."""

    id: PydanticObjectId


class IdAlias:
    """Model for generic ID alias."""

    id: PydanticObjectId = Field(..., alias="_id")


class IdDefaultFactory:
    """Model for generic ID with default factory."""

    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")


class CafeId:
    """Model for cafe ID."""

    cafe_id: PydanticObjectId


class CategoryId:
    """Model for category ID."""

    category_id: Optional[PydanticObjectId] = None


class ItemId:
    """Model for item ID."""

    item_id: PydanticObjectId


class UserId:
    """Model for user ID."""

    user_id: PydanticObjectId


class ErrorDetail(BaseModel):
    """Model for error detail."""

    msg: str


class ErrorResponse(BaseModel):
    """Model for error response."""

    detail: Optional[List[ErrorDetail]]


class ErrorConflictDetail(BaseModel):
    """Model for conflict detail."""

    msg: str
    fields: List[str]


class ErrorConflictResponse(BaseModel):
    """Model for conflict response."""

    detail: Optional[List[ErrorConflictDetail]]
