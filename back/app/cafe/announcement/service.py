"""
Module for handling announcement-related operations.
"""

from typing import List, Union

from beanie import PydanticObjectId
from beanie.odm.queries.find import FindMany

from app.cafe.announcement.models import (
    Announcement,
    AnnouncementCreate,
    AnnouncementUpdate,
    AnnouncementView,
)
from app.cafe.models import Cafe
from app.service import set_attributes
from app.user.models import User


class AnnouncementService:
    """Service class for announcement operations."""

    async def get_all(
        to_list: bool = True,
        as_view: bool = False,
        **filters: dict,
    ) -> Union[FindMany[Announcement], List[Announcement]]:
        """Get announcements."""
        announcement_class = AnnouncementView if as_view else Announcement
        sort_by = filters.pop("sort_by", "start_date")
        query = announcement_class.find(filters).sort(sort_by)
        return await query.to_list() if to_list else query

    async def get(
        id: PydanticObjectId,
        as_view: bool = False,
    ) -> Union[AnnouncementView, Announcement]:
        """Get an announcement by ID."""
        announcement_class = AnnouncementView if as_view else Announcement
        return await announcement_class.get(id)

    async def get_by_id_and_cafe_id(
        id: PydanticObjectId,
        cafe_id: PydanticObjectId,
        as_view: bool = False,
    ) -> Union[AnnouncementView, Announcement]:
        """Get an announcement by ID and cafe ID."""
        announcement_class = AnnouncementView if as_view else Announcement
        return await announcement_class.find_one({"_id": id, "cafe_id": cafe_id})

    async def create(
        current_user: User,
        cafe: Cafe,
        data: AnnouncementCreate,
    ) -> Announcement:
        """Create a new announcement."""
        announcement = Announcement(
            **data.model_dump(), cafe_id=cafe.id, author_id=current_user.id
        )
        await announcement.insert()
        return announcement

    async def update(
        announcement: Announcement,
        data: AnnouncementUpdate,
    ) -> Announcement:
        """Update an existing announcement."""
        set_attributes(announcement, data)
        await announcement.save()
        return announcement

    async def delete(announcement: Announcement) -> None:
        """Delete an announcement."""
        await announcement.delete()
