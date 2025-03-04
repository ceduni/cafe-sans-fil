"""
Module for handling event-related operations.
"""

from typing import List, Literal, Union, overload

from beanie import PydanticObjectId
from beanie.odm.queries.find import FindMany

from app.cafe.event.models import Event, EventCreate, EventUpdate, EventView
from app.cafe.models import Cafe
from app.service import set_attributes
from app.user.models import User


class EventService:
    """Service class for Event operations."""

    @overload
    @staticmethod
    async def get_all(
        to_list: Literal[True] = True,
        as_view: Literal[False] = False,
        **filters: dict,
    ) -> List[Event]: ...

    @overload
    @staticmethod
    async def get_all(
        to_list: Literal[False],
        as_view: Literal[False] = False,
        **filters: dict,
    ) -> FindMany[Event]: ...

    @overload
    @staticmethod
    async def get_all(
        to_list: Literal[True],
        as_view: Literal[True],
        **filters: dict,
    ) -> List[EventView]: ...

    @overload
    @staticmethod
    async def get_all(
        to_list: Literal[False],
        as_view: Literal[True],
        **filters: dict,
    ) -> FindMany[EventView]: ...

    @staticmethod
    async def get_all(
        to_list: bool = True,
        as_view: bool = False,
        **filters: dict,
    ) -> List[Event] | FindMany[Event] | List[EventView] | FindMany[EventView]:
        """Get events."""
        event_class = EventView if as_view else Event
        sort_by = filters.pop("sort_by", "-start_date")
        query = event_class.find(filters).sort(sort_by)
        return await query.to_list() if to_list else query

    @staticmethod
    async def get(
        id: PydanticObjectId,
        as_view: bool = False,
    ) -> Union[Event, EventView]:
        """Get an event by ID."""
        event_class = EventView if as_view else Event
        id_field = "id" if as_view else "_id"
        return await event_class.find_one({id_field: id})

    @staticmethod
    async def get_by_id_and_cafe_id(
        id: PydanticObjectId,
        cafe_id: PydanticObjectId,
        as_view: bool = False,
    ) -> Union[Event, EventView]:
        """Get an event by ID and cafe ID."""
        event_class = EventView if as_view else Event
        id_field = "id" if as_view else "_id"
        return await event_class.find_one({id_field: id, "cafe_id": cafe_id})

    @staticmethod
    async def create(
        current_user: User,
        cafe: Cafe,
        data: EventCreate,
    ) -> Event:
        """Create an event."""
        event = Event(**data.model_dump(), cafe_id=cafe.id, creator_id=current_user.id)
        await event.insert()
        return event

    @staticmethod
    async def update(
        event: Event,
        data: EventUpdate,
    ) -> Event:
        """Update an event."""
        set_attributes(event, data)
        await event.save()
        return event

    @staticmethod
    async def delete(event: Event) -> None:
        """Delete an event."""
        await event.delete()
        return event
