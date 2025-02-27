"""
Module for global models.
"""

from typing import List, Optional

from beanie import Document, PydanticObjectId
from beanie.exceptions import RevisionIdWasChanged
from pydantic import BaseModel, Field
from pymongo.errors import DuplicateKeyError


class Id:
    """Model for generic ID."""

    id: PydanticObjectId


class IdOptional:
    """Model for optional generic ID."""

    id: Optional[PydanticObjectId] = None


class IdAlias:
    """Model for generic ID alias."""

    id: Optional[PydanticObjectId] = Field(None, alias="_id")


class IdDefaultFactory:
    """Model for generic ID with default factory."""

    id: Optional[PydanticObjectId] = Field(
        default_factory=PydanticObjectId, alias="_id"
    )


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


class CustomDocument(Document):
    """Base class for Beanie documents."""

    async def insert(self, *args, **kwargs):
        """Catch and re-raise duplicate key errors."""
        try:
            return await super().insert(*args, **kwargs)
        except RevisionIdWasChanged as e:
            if isinstance(e.__context__, DuplicateKeyError):
                raise e.__context__
            else:
                raise e

    async def save(self, *args, **kwargs):
        """Catch and re-raise duplicate key errors."""
        try:
            return await super().save(*args, **kwargs)
        except RevisionIdWasChanged as e:
            if isinstance(e.__context__, DuplicateKeyError):
                raise e.__context__
            else:
                raise e
