"""
Module for handling cafe-related operations.
"""

from typing import List, Union

from beanie import PydanticObjectId
from beanie.odm.queries.find import FindMany
from bson.errors import InvalidId

from app.cafe.models import Cafe, CafeCreate, CafeUpdate, CafeView
from app.cafe.staff.enums import Role
from app.cafe.staff.service import StaffService
from app.service import set_attributes


class CafeService:
    """Service for CRUD operations and search on Cafe."""

    @staticmethod
    async def get_all(
        to_list: bool = True, **filters: dict
    ) -> Union[FindMany[Cafe], List[Cafe]]:
        """Get cafes."""
        sort_by = filters.pop("sort_by", "name")
        query = Cafe.find(filters).sort(sort_by)
        return await query.to_list() if to_list else query

    @staticmethod
    async def get(cafe_slug_or_id: str, as_view: bool = False):
        """Get a cafe by slug or ID."""
        cafe_class = CafeView if as_view else Cafe
        try:
            id = PydanticObjectId(cafe_slug_or_id)
            return await cafe_class.find_one({"_id": id})
        except InvalidId:
            slug = cafe_slug_or_id
            return await cafe_class.find_one(
                {
                    "$or": [
                        {"slug": slug},
                        {"previous_slugs": slug},
                    ]
                }
            )

    @staticmethod
    async def create(data: CafeCreate, owner_id: PydanticObjectId) -> Cafe:
        """Create a new cafe."""
        cafe = Cafe(**data.model_dump(), owner_id=owner_id)
        return await cafe.insert()

    @staticmethod
    async def update(cafe: Cafe, data: CafeUpdate):
        """Update a cafe."""
        # Check if owner is changing
        if data.owner_id and data.owner_id != cafe.owner_id:
            # Update previous owner as admin
            await StaffService.add(cafe, Role.ADMIN, cafe.owner_id)

            # Remove previous role for new owner
            if data.owner_id in cafe.staff.admin_ids:
                await StaffService.remove(cafe, Role.ADMIN, data.owner_id)
            if data.owner_id in cafe.staff.volunteer_ids:
                await StaffService.remove(cafe, Role.VOLUNTEER, data.owner_id)

        set_attributes(cafe, data)
        await cafe.save()
        return cafe
