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


class CafeId:
    """Model for cafe ID."""

    cafe_id: PydanticObjectId


class ItemId:
    """Model for item ID."""

    item_id: PydanticObjectId


class UserId:
    """Model for user ID."""

    user_id: PydanticObjectId
