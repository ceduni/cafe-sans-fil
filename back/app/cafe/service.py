"""
Module for handling cafe-related operations.
"""

from typing import List

from beanie import PydanticObjectId
from bson.errors import InvalidId

from app.cafe.models import (
    Cafe,
    CafeCreate,
    CafeUpdate,
    CafeView,
    Role,
    StaffCreate,
    StaffMember,
    StaffUpdate,
)
from app.user.models import User


class CafeService:
    """Service for CRUD operations and search on Cafe."""

    # --------------------------------------
    #               Cafe
    # --------------------------------------

    @staticmethod
    async def get_all(**filters: dict):
        """Get cafes."""
        sort_by = filters.pop("sort_by", "name")
        return Cafe.find(filters).sort(sort_by)

    @staticmethod
    async def get(cafe_slug_or_id: str, as_view: bool = False):
        """Get a cafe by slug or ID."""
        cafe_class = CafeView if as_view else Cafe
        try:
            cafe_id = PydanticObjectId(cafe_slug_or_id)
            return await cafe_class.find_one({"_id": cafe_id})
        except InvalidId:
            return await cafe_class.find_one(
                {
                    "$or": [
                        {"slug": cafe_slug_or_id},
                        {"previous_slugs": cafe_slug_or_id},
                    ]
                }
            )

    @staticmethod
    async def create(data: CafeCreate) -> Cafe:
        """Create a new cafe."""
        try:
            cafe = Cafe(**data.model_dump())
            await cafe.insert()
            return cafe
        except Exception as e:
            if "duplicate" in str(e).lower() and len(str(e)) < 100:
                raise ValueError("Cafe already exists")

    @staticmethod
    async def update(cafe: Cafe, data: CafeUpdate):
        """Update a cafe."""
        try:
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(cafe, field, value)
            await cafe.save()
            return cafe
        except Exception as e:
            raise ValueError(e)

    # --------------------------------------
    #               Staff
    # --------------------------------------

    @staticmethod
    async def get_staff(cafe: Cafe, username: str):
        """Get a staff member by username from a cafe."""
        for member in cafe.staff:
            if member.username == username:
                return member

        raise ValueError("Staff member not found")

    @staticmethod
    async def create_staff(cafe: Cafe, data: StaffCreate):
        """Create a new staff member for a cafe."""
        new_staff_member = StaffMember(**data.model_dump())
        cafe.staff.append(new_staff_member)
        await cafe.save()
        return new_staff_member

    @staticmethod
    async def update_staff(cafe: Cafe, username: str, data: StaffUpdate):
        """Update a staff member for a cafe."""
        for member in cafe.staff:
            if member.username == username:
                for key, value in data.model_dump(exclude_unset=True).items():
                    setattr(member, key, value)
                await cafe.save()
                return member

        raise ValueError("Staff member not found")

    @staticmethod
    async def delete_staff(cafe: Cafe, username: str):
        """Delete a staff member from a cafe."""
        if any(member.username == username for member in cafe.staff):
            cafe.staff = [
                member for member in cafe.staff if member.username != username
            ]
            await cafe.save()
        else:
            raise ValueError("Staff member not found")

    @staticmethod
    async def create_many_staff(
        cafe: Cafe, datas: List[StaffCreate]
    ) -> List[StaffMember]:
        """Create multiple staff members for a cafe."""
        new_staff_members = [
            StaffMember(**staff_data.model_dump()) for staff_data in datas
        ]
        cafe.staff.extend(new_staff_members)
        await cafe.save()
        return new_staff_members

    @staticmethod
    async def update_many_staff(
        cafe: Cafe, usernames: List[str], data: StaffUpdate
    ) -> List[StaffMember]:
        """Update multiple staff members for a cafe."""
        updated_members = []
        for member in cafe.staff:
            if member.username in usernames:
                for key, value in data.model_dump(exclude_unset=True).items():
                    setattr(member, key, value)
                updated_members.append(member)

        if not updated_members:
            raise ValueError("No staff members found for the provided usernames")

        await cafe.save()
        return updated_members

    @staticmethod
    async def delete_many_staff(cafe: Cafe, usernames: List[str]) -> None:
        """Delete multiple staff members from a cafe."""
        cafe.staff = [
            member for member in cafe.staff if member.username not in usernames
        ]
        await cafe.save()

    # --------------------------------------
    #               Authorization
    # --------------------------------------

    @staticmethod
    async def is_authorized_for_cafe_action(
        cafe: Cafe, current_user: User, required_roles: List[Role]
    ):
        """Check if a user is authorized to perform an action on a cafe."""
        # Check if part of staff
        user_in_staff = None
        for user in cafe.staff:
            if user.username == current_user.username:
                user_in_staff = user
                break

        # Check if appropriate role
        if user_in_staff:
            if user_in_staff.role not in [role.value for role in required_roles]:
                raise ValueError("Access forbidden")
        else:
            raise ValueError("Access forbidden")

        return True
