"""
Module for handling staff-related models.
"""

from typing import List

from beanie import PydanticObjectId
from pydantic import BaseModel

from app.user.models import UserView, UserViewOut


class Staff(BaseModel):
    admin_ids: List[PydanticObjectId] = []
    volunteer_ids: List[PydanticObjectId] = []


class StaffView(BaseModel):
    admins: List[UserView] = []
    volunteers: List[UserView] = []


class StaffViewOut(BaseModel):
    admins: List[UserViewOut] = []
    volunteers: List[UserViewOut] = []
