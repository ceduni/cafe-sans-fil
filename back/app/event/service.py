"""
Module for handling event-related operations.
"""

from beanie import PydanticObjectId

from app.event.models import Event, EventCreate, EventOut, UserInteraction


class EventService:
    """Service class for Event operations."""

    async def get_all(**filters: dict):
        """Get events."""
        sort_by = filters.pop("sort_by", "start_date")
        return Event.find(filters).sort(sort_by)

    async def get(id: PydanticObjectId) -> EventOut:
        """Get an event by ID."""
        return await Event.get(id)

    async def create(data: EventCreate) -> EventOut:
        """Create a new event."""
        event = Event(**data.model_dump())
        await event.insert()
        return event

    async def update(event: Event, data: EventCreate) -> EventOut:
        """Update an existing event."""
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(event, key, value)
        await event.save()
        return event

    async def delete(event: Event) -> EventOut:
        """Delete an existing event."""
        await event.delete()
        return event

    async def add_attendee(event: Event, id: PydanticObjectId) -> EventOut:
        """Add an attendee to an event."""
        if not any(att.user_id == id for att in event.attendees):
            event.attendees.append(UserInteraction(user_id=id))
            await event.save()
        return event

    async def add_supporter(event: Event, id: PydanticObjectId) -> EventOut:
        """Add a supporter to an event."""
        if not any(sup.user_id == id for sup in event.supporters):
            event.supporters.append(UserInteraction(user_id=id))
            await event.save()
        return event

    async def remove_attendee(event: Event, id: PydanticObjectId) -> EventOut:
        """Remove an attendee from an event."""
        original_attendees = len(event.attendees)
        event.attendees = [
            attendee for attendee in event.attendees if attendee.user_id != id
        ]
        if len(event.attendees) < original_attendees:
            await event.save()
        return event

    async def remove_supporter(event: Event, id: PydanticObjectId) -> EventOut:
        """Remove a supporter from an event."""
        original_supporters = len(event.supporters)
        event.supporters = [
            supporter for supporter in event.supporters if supporter.user_id != id
        ]
        if len(event.supporters) < original_supporters:
            await event.save()
        return event
