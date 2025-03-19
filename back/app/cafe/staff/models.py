"""
Module for handling staff-related models.
"""

from typing import List

from beanie import PydanticObjectId
from pydantic import BaseModel

from app.user.models import UserOut


class Staff(BaseModel):
    """Model for cafe staff."""

    admin_ids: List[PydanticObjectId] = []
    volunteer_ids: List[PydanticObjectId] = []


class StaffOut(BaseModel):
    """Model for cafe staff output."""

    admins: List[UserOut] = []
    volunteers: List[UserOut] = []


class StaffWithOwnerOut(BaseModel):
    """Model for cafe staff with owner output."""

    owner: UserOut
    admins: List[UserOut] = []
    volunteers: List[UserOut] = []
