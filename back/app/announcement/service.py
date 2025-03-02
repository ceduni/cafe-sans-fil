"""
Module for handling announcement-related operations.
"""

from typing import List, Union

from beanie import PydanticObjectId
from beanie.odm.queries.find import FindMany

from app.announcement.models import (
    Announcement,
    AnnouncementCreate,
    AnnouncementOut,
    UserInteraction,
)


class AnnouncementService:
    """Service class for announcement operations."""

    async def get_all(
        to_list: bool = True, **filters: dict
    ) -> Union[FindMany[Announcement], List[Announcement]]:
        """Get announcements."""
        sort_by = filters.pop("sort_by", "start_date")
        query = Announcement.find(filters).sort(sort_by)
        return await query.to_list() if to_list else query

    async def get(id: PydanticObjectId) -> AnnouncementOut:
        """Get an announcement by ID."""
        return await Announcement.get(id)

    async def create(
        data: AnnouncementCreate,
    ) -> Announcement:
        """Create a new announcement."""
        announcement = Announcement(**data.model_dump())
        await announcement.insert()
        return announcement

    async def update(
        announcement: Announcement, data: AnnouncementCreate
    ) -> Announcement:
        """Update an existing announcement."""
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(announcement, key, value)
        await announcement.save()
        return announcement

    async def delete(announcement: Announcement) -> None:
        """Delete an announcement."""
        await announcement.delete()

    async def add_like(
        announcement: Announcement, id: PydanticObjectId
    ) -> AnnouncementOut:
        """Add a like to an announcement."""
        if not any(li.user_id == id for li in announcement.likes):
            announcement.likes.append(UserInteraction(user_id=id))
            await announcement.save()
        return announcement

    async def remove_like(
        announcement: Announcement, id: PydanticObjectId
    ) -> AnnouncementOut:
        """Remove a like from an announcement."""
        original_likes = len(announcement.likes)
        announcement.likes = [like for like in announcement.likes if like.user_id != id]
        if len(announcement.likes) < original_likes:
            await announcement.save()
        return announcement
