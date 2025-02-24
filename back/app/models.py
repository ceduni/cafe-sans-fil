"""
Module for global models.
"""

from beanie import PydanticObjectId
from pydantic import Field


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

    category_id: PydanticObjectId


class ItemId:
    """Model for item ID."""

    item_id: PydanticObjectId


class UserId:
    """Model for user ID."""

    user_id: PydanticObjectId
