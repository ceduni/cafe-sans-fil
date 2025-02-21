"""
Module for global models.
"""

from beanie import PydanticObjectId
from pydantic import Field


class Id:
    id: PydanticObjectId


class IdAlias:
    id: PydanticObjectId = Field(..., alias="_id")


class CafeId:
    cafe_id: PydanticObjectId


class ItemId:
    item_id: PydanticObjectId


class UserId:
    user_id: PydanticObjectId
