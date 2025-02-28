"""
Module for handling staff-related operations.
"""

from typing import List

from beanie import PydanticObjectId

from app.cafe.models import Cafe
from app.cafe.staff.enums import Role


class StaffService:
    """Service for CRUD operations and search on Staff."""

    @staticmethod
    async def is_staff(cafe: Cafe, id: PydanticObjectId) -> bool:
        """Check if a user is a staff member of a cafe."""
        return (
            id == cafe.owner_id
            or id in cafe.staff.admin_ids
            or id in cafe.staff.volunteer_ids
        )

    @staticmethod
    async def add(cafe: Cafe, role: Role, id: PydanticObjectId) -> None:
        """Add a staff member to a cafe."""
        staff_list = (
            cafe.staff.admin_ids
            if role.upper() == Role.ADMIN
            else cafe.staff.volunteer_ids
        )
        if id not in staff_list:
            staff_list.append(id)
            await cafe.save()

    @staticmethod
    async def remove(cafe: Cafe, role: Role, id: PydanticObjectId) -> None:
        """Remove a staff member from a cafe."""
        staff_list = (
            cafe.staff.admin_ids
            if role.upper() == Role.ADMIN
            else cafe.staff.volunteer_ids
        )
        if id in staff_list:
            staff_list.remove(id)
            await cafe.save()

    @staticmethod
    async def add_many(cafe: Cafe, role: Role, ids: List[PydanticObjectId]) -> None:
        """Add multiple staff members to a cafe."""
        staff_list = (
            cafe.staff.admin_ids
            if role.upper() == Role.ADMIN
            else cafe.staff.volunteer_ids
        )
        new_ids = [id for id in ids if id not in staff_list]
        if new_ids:
            staff_list.extend(new_ids)
            await cafe.save()

    @staticmethod
    async def remove_many(cafe: Cafe, role: Role, ids: List[PydanticObjectId]) -> None:
        """Remove multiple staff members from a cafe."""
        staff_list = (
            cafe.staff.admin_ids
            if role.upper() == Role.ADMIN
            else cafe.staff.volunteer_ids
        )
        original_count = len(staff_list)
        staff_list[:] = [id for id in staff_list if id not in ids]
        if len(staff_list) != original_count:
            await cafe.save()
