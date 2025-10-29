"""
Module for handling staff-related operations.
"""

from typing import List, Optional

from beanie import PydanticObjectId
from bson.errors import InvalidId

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
    async def get(cafe_slug_or_id: str, role: str = None) -> Optional[dict]:
        """Get all staff members of a cafe."""
        try:
            cafe_id = PydanticObjectId(cafe_slug_or_id)
            filters = {"_id": cafe_id}
        except InvalidId:
            filters = {
                "$or": [{"slug": cafe_slug_or_id}, {"previous_slugs": cafe_slug_or_id}]
            }

        pipeline = StaffService._build_pipeline(filters=filters)
        result = await Cafe.aggregate(pipeline).to_list()
        return result[0] if result else None

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

    @staticmethod
    def _build_pipeline(filters: Optional[dict] = None) -> list:
        """Build aggregation pipeline."""
        pipeline = []
        filters = filters or {}

        if filters:
            pipeline.append({"$match": filters})

        pipeline.extend(
            [
                # Lookup owner
                {
                    "$lookup": {
                        "from": "users",
                        "localField": "owner_id",
                        "foreignField": "_id",
                        "pipeline": [
                            {
                                "$project": {
                                    "_id": 0,
                                    "id": "$_id",
                                    "username": 1,
                                    "email": 1,
                                    "first_name": 1,
                                    "last_name": 1,
                                    "photo_url": 1,
                                }
                            }
                        ],
                        "as": "owner",
                    }
                },
                # Lookup admins
                {
                    "$lookup": {
                        "from": "users",
                        "localField": "staff.admin_ids",
                        "foreignField": "_id",
                        "pipeline": [
                            {
                                "$project": {
                                    "_id": 0,
                                    "id": "$_id",
                                    "username": 1,
                                    "email": 1,
                                    "first_name": 1,
                                    "last_name": 1,
                                    "photo_url": 1,
                                }
                            }
                        ],
                        "as": "admins",
                    }
                },
                # Lookup volunteers
                {
                    "$lookup": {
                        "from": "users",
                        "localField": "staff.volunteer_ids",
                        "foreignField": "_id",
                        "pipeline": [
                            {
                                "$project": {
                                    "_id": 0,
                                    "id": "$_id",
                                    "username": 1,
                                    "email": 1,
                                    "first_name": 1,
                                    "last_name": 1,
                                    "photo_url": 1,
                                }
                            }
                        ],
                        "as": "volunteers",
                    }
                },
                # Add owner and staff
                {"$addFields": {"owner": {"$arrayElemAt": ["$owner", 0]}}},
                {"$addFields": {"id": "$_id"}},
                # Clean up temporary fields
                {
                    "$unset": [
                        "_id",
                        "owner_id",
                        "staff",
                    ]
                },
            ]
        )

        return pipeline
