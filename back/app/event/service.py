"""
Module for handling event-related operations.
"""

from typing import List

from beanie import PydanticObjectId

from app.event.models import Event, EventCreate, EventOut, UserInteraction


class EventService:
    """Service class for Event operations."""

    async def get_events(**filters: dict):
        """Get events."""
        sort_by = filters.pop("sort_by", "start_date")
        return Event.find(filters).sort(sort_by)

    async def create_event(event_data: EventCreate) -> EventOut:
        """Create a new event."""
        event = Event(**event_data.model_dump())
        await event.insert()
        return event

    async def update_event(
        event_id: PydanticObjectId, event_data: EventCreate
    ) -> EventOut:
        """Update an existing event."""
        event = await Event.find_one(Event.id == event_id)
        if not event:
            raise ValueError("Event not found")
        for key, value in event_data.dict(exclude_unset=True).items():
            setattr(event, key, value)
        await event.save()
        return event

    async def remove_event(event_id: PydanticObjectId) -> EventOut:
        """Delete an existing event."""
        event = await Event.find_one(Event.id == event_id)
        if not event:
            raise ValueError("Event not found")
        await event.delete()
        return event

    async def add_attendee_to_event(
        event_id: PydanticObjectId, user_id: PydanticObjectId
    ) -> EventOut:
        """Add an attendee to an event."""
        event = await Event.find_one(Event.id == event_id)
        if not event:
            raise ValueError("Event not found")
        if not any(att.user_id == user_id for att in event.attendees):
            event.attendees.append(UserInteraction(user_id=user_id))
            await event.save()
        return event

    async def add_supporter_to_event(
        event_id: PydanticObjectId, user_id: PydanticObjectId
    ) -> EventOut:
        """Add a supporter to an event."""
        event = await Event.find_one(Event.id == event_id)
        if not event:
            raise ValueError("Event not found")
        if not any(sup.user_id == user_id for sup in event.supporters):
            event.supporters.append(UserInteraction(user_id=user_id))
            await event.save()
        return event

    async def remove_attendee_from_event(
        event_id: PydanticObjectId, user_id: PydanticObjectId
    ) -> EventOut:
        """Remove an attendee from an event."""
        event = await Event.find_one(Event.id == event_id)
        if not event:
            raise ValueError("Event not found")
        original_attendees = len(event.attendees)
        event.attendees = [
            attendee for attendee in event.attendees if attendee.user_id != user_id
        ]
        if len(event.attendees) < original_attendees:
            await event.save()
        return event

    async def remove_supporter_from_event(
        event_id: PydanticObjectId, user_id: PydanticObjectId
    ) -> EventOut:
        """Remove a supporter from an event."""
        event = await Event.find_one(Event.id == event_id)
        if not event:
            raise ValueError("Event not found")
        original_supporters = len(event.supporters)
        event.supporters = [
            supporter for supporter in event.supporters if supporter.user_id != user_id
        ]
        if len(event.supporters) < original_supporters:
            await event.save()
        return event
