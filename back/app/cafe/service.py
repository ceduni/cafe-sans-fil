"""
Module for handling cafe-related operations.
"""

from typing import List

from beanie import PydanticObjectId
from bson.errors import InvalidId

from app.cafe.models import Cafe, CafeView, Role, StaffMember
from app.cafe.schemas import (
    CafeCreate,
    CafeShortOut,
    CafeUpdate,
    StaffCreate,
    StaffUpdate,
)
from app.user.models import User


class CafeService:
    """Service for CRUD operations and search on Cafe."""

    # --------------------------------------
    #               Cafe
    # --------------------------------------

    @staticmethod
    async def list_cafes(**query_params) -> List[Cafe]:
        """List cafes based on the provided query parameters."""
        sort_by = query_params.pop("sort_by", "name")
        page = int(query_params.pop("page", 1))
        limit = int(query_params.pop("limit", 40))
        return (
            await Cafe.find(query_params)
            .skip((page - 1) * limit)
            .limit(limit)
            .sort(sort_by)
            .to_list()
        )

    @staticmethod
    async def retrieve_cafe(cafe_slug_or_id, as_view: bool = True):
        """Retrieve a cafe by slug or ID."""
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
    async def create_cafe(data: CafeCreate) -> Cafe:
        """Create a new cafe."""
        try:
            cafe = Cafe(**data.model_dump())
            await cafe.insert()
            return cafe
        except Exception as e:
            if "duplicate" in str(e).lower() and len(str(e)) < 100:
                raise ValueError("Cafe already exists")

    @staticmethod
    async def update_cafe(cafe_id: PydanticObjectId, data: CafeUpdate):
        """Update a cafe."""
        try:
            cafe = await Cafe.find_one({"_id": cafe_id})
            if not cafe:
                raise ValueError("Cafe not found")

            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(cafe, field, value)
            await cafe.save()
            return cafe
        except Exception as e:
            if "duplicate" in str(e).lower() and len(str(e)) < 100:
                raise ValueError(e)
            else:
                raise ValueError("Cafe already exists")

    # --------------------------------------
    #               Staff
    # --------------------------------------

    @staticmethod
    async def list_staff_members(cafe_id: PydanticObjectId):
        """List staff members of a cafe."""
        cafe = await Cafe.find_one({"_id": cafe_id})
        if not cafe:
            raise ValueError("Cafe not found")
        return cafe.staff

    @staticmethod
    async def retrieve_staff_member(cafe_id: PydanticObjectId, username: str):
        """Retrieve a staff member by username from a cafe."""
        cafe = await Cafe.find_one({"_id": cafe_id})
        if not cafe:
            raise ValueError("Cafe not found")

        for member in cafe.staff:
            if member.username == username:
                return member

        raise ValueError("Staff member not found")

    @staticmethod
    async def create_staff_member(cafe_id: PydanticObjectId, staff_data: StaffCreate):
        """Create a new staff member for a cafe."""
        cafe = await Cafe.find_one({"_id": cafe_id})
        if not cafe:
            raise ValueError("Cafe not found")

        new_staff_member = StaffMember(**staff_data.model_dump())
        cafe.staff.append(new_staff_member)
        await cafe.save()
        return new_staff_member

    @staticmethod
    async def update_staff_member(
        cafe_id: PydanticObjectId, username: str, staff_data: StaffUpdate
    ):
        """Update a staff member for a cafe."""
        cafe = await Cafe.find_one({"_id": cafe_id})
        if not cafe:
            raise ValueError("Cafe not found")

        for member in cafe.staff:
            if member.username == username:
                for key, value in staff_data.model_dump(exclude_unset=True).items():
                    setattr(member, key, value)
                await cafe.save()
                return member

        raise ValueError("Staff member not found")

    @staticmethod
    async def delete_staff_member(cafe_id: PydanticObjectId, username: str):
        """Delete a staff member from a cafe."""
        cafe = await Cafe.find_one({"_id": cafe_id})
        if not cafe:
            raise ValueError("Cafe not found")

        if any(member.username == username for member in cafe.staff):
            cafe.staff = [
                member for member in cafe.staff if member.username != username
            ]
            await cafe.save()
        else:
            raise ValueError("Staff member not found")

    @staticmethod
    async def create_many_staff_members(
        cafe_id: PydanticObjectId, staff_data_list: List[StaffCreate]
    ) -> List[StaffMember]:
        """Create multiple staff members for a cafe."""
        cafe = await Cafe.find_one({"_id": cafe_id})
        if not cafe:
            raise ValueError("Cafe not found")

        new_staff_members = [
            StaffMember(**staff_data.model_dump()) for staff_data in staff_data_list
        ]
        cafe.staff.extend(new_staff_members)
        await cafe.save()
        return new_staff_members

    @staticmethod
    async def update_many_staff_members(
        cafe_id: PydanticObjectId, usernames: List[str], staff_data: StaffUpdate
    ) -> List[StaffMember]:
        """Update multiple staff members for a cafe."""
        cafe = await Cafe.find_one({"_id": cafe_id})
        if not cafe:
            raise ValueError("Cafe not found")

        updated_members = []
        for member in cafe.staff:
            if member.username in usernames:
                for key, value in staff_data.model_dump(exclude_unset=True).items():
                    setattr(member, key, value)
                updated_members.append(member)

        if not updated_members:
            raise ValueError("No staff members found for the provided usernames")

        await cafe.save()
        return updated_members

    @staticmethod
    async def delete_many_staff_members(
        cafe_id: PydanticObjectId, usernames: List[str]
    ) -> None:
        """Delete multiple staff members from a cafe."""
        cafe = await Cafe.find_one({"_id": cafe_id})
        if not cafe:
            raise ValueError("Cafe not found")

        cafe.staff = [
            member for member in cafe.staff if member.username not in usernames
        ]
        await cafe.save()

    # --------------------------------------
    #               Authorization
    # --------------------------------------

    @staticmethod
    async def is_authorized_for_cafe_action(
        cafe_id: PydanticObjectId, current_user: User, required_roles: List[Role]
    ):
        """Check if a user is authorized to perform an action on a cafe."""
        cafe = await Cafe.find_one({"_id": cafe_id})
        if not cafe:
            raise ValueError("Cafe not found")

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
