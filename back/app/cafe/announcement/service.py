"""
Module for handling announcement-related operations.
"""

from typing import List, Literal, Union, overload

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

    @overload
    @staticmethod
    async def get_all(
        to_list: Literal[True] = True,
        as_view: Literal[False] = False,
        **filters: dict,
    ) -> List[Announcement]: ...

    @overload
    @staticmethod
    async def get_all(
        to_list: Literal[False],
        as_view: Literal[False] = False,
        **filters: dict,
    ) -> FindMany[Announcement]: ...

    @overload
    @staticmethod
    async def get_all(
        to_list: Literal[True],
        as_view: Literal[True],
        **filters: dict,
    ) -> List[AnnouncementView]: ...

    @overload
    @staticmethod
    async def get_all(
        to_list: Literal[False],
        as_view: Literal[True],
        **filters: dict,
    ) -> FindMany[AnnouncementView]: ...

    @staticmethod
    async def get_all(
        to_list: bool = True,
        as_view: bool = False,
        **filters: dict,
    ) -> (
        List[Announcement]
        | FindMany[Announcement]
        | List[AnnouncementView]
        | FindMany[AnnouncementView]
    ):
        """Get announcements."""
        announcement_class = AnnouncementView if as_view else Announcement
        sort_by = filters.pop("sort_by", "-updated_at")
        query = announcement_class.find(filters).sort(sort_by)
        return await query.to_list() if to_list else query

    @staticmethod
    async def get(
        id: PydanticObjectId,
        as_view: bool = False,
    ) -> Union[Announcement, AnnouncementView]:
        """Get an announcement by ID."""
        announcement_class = AnnouncementView if as_view else Announcement
        id_field = "id" if as_view else "_id"
        return await announcement_class.find_one({id_field: id})

    @staticmethod
    async def get_by_id_and_cafe_id(
        id: PydanticObjectId,
        cafe_id: PydanticObjectId,
        as_view: bool = False,
    ) -> Union[Announcement, AnnouncementView]:
        """Get an announcement by ID and cafe ID."""
        announcement_class = AnnouncementView if as_view else Announcement
        id_field = "id" if as_view else "_id"
        return await announcement_class.find_one({id_field: id, "cafe_id": cafe_id})

    @staticmethod
    async def create(
        current_user: User,
        cafe: Cafe,
        data: AnnouncementCreate,
    ) -> Announcement:
        """Create an announcement."""
        announcement = Announcement(
            **data.model_dump(), cafe_id=cafe.id, author_id=current_user.id
        )
        await announcement.insert()
        return announcement

    @staticmethod
    async def update(
        announcement: Announcement,
        data: AnnouncementUpdate,
    ) -> Announcement:
        """Update an announcement."""
        set_attributes(announcement, data)
        await announcement.save()
        return announcement

    @staticmethod
    async def delete(announcement: Announcement) -> None:
        """Delete an announcement."""
        await announcement.delete()
