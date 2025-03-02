"""
Module for handling event-related operations.
"""

from typing import List, Union

from beanie import PydanticObjectId
from beanie.odm.queries.find import FindMany

from app.cafe.models import Cafe
from app.event.models import Event, EventCreate, EventUpdate, EventView
from app.service import set_attributes
from app.user.models import User


class EventService:
    """Service class for Event operations."""

    async def get_all(
        to_list: bool = True,
        as_view: bool = False,
        **filters: dict,
    ) -> Union[FindMany[Event], List[Event]]:
        """Get events."""
        event_class = EventView if as_view else Event
        sort_by = filters.pop("sort_by", "start_date")
        query = event_class.find(filters).sort(sort_by)
        return await query.to_list() if to_list else query

    async def get(
        id: PydanticObjectId,
        as_view: bool = False,
    ) -> Union[EventView, Event]:
        """Get an event by ID."""
        event_class = EventView if as_view else Event
        return await event_class.get(id)

    async def get_by_id_and_cafe_id(
        id: PydanticObjectId,
        cafe_id: PydanticObjectId,
        as_view: bool = False,
    ) -> Union[EventView, Event]:
        """Get an event by ID and cafe ID."""
        event_class = EventView if as_view else Event
        return await event_class.find_one({"_id": id, "cafe_id": cafe_id})

    async def create(
        current_user: User,
        cafe: Cafe,
        data: EventCreate,
    ) -> Event:
        """Create a new event."""
        event = Event(**data.model_dump(), cafe_id=cafe.id, creator_id=current_user.id)
        await event.insert()
        return event

    async def update(
        event: Event,
        data: EventUpdate,
    ) -> Event:
        """Update an existing event."""
        set_attributes(event, data)
        await event.save()
        return event

    async def delete(event: Event) -> None:
        """Delete an existing event."""
        await event.delete()
        return event
