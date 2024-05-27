from typing import List
from app.models.event_model import Event, UserInteraction
from app.schemas.event_schema import EventCreate, EventOut
from uuid import UUID

class EventService:
    async def get_events(**query_params) -> List[EventOut]:
        sort_by = query_params.pop("sort_by", "start_date")
        page = int(query_params.pop("page", 1))
        limit = int(query_params.pop("limit", 9))
        return (
            await Event.find(query_params)
            .skip((page - 1) * limit)
            .limit(limit)
            .sort(sort_by)
            .to_list()
        )

    async def create_event(event_data: EventCreate) -> EventOut:
        event = Event(**event_data.model_dump())
        await event.insert()
        return event

    async def update_event(event_id: UUID, event_data: EventCreate) -> EventOut:
        event = await Event.find_one(Event.event_id == event_id)
        if not event:
            raise ValueError("Event not found")
        for key, value in event_data.dict(exclude_unset=True).items():
            setattr(event, key, value)
        await event.save()
        return event

    async def remove_event(event_id: UUID) -> EventOut:
        event = await Event.find_one(Event.event_id == event_id)
        if not event:
            raise ValueError("Event not found")
        await event.delete()
        return event
    
    async def add_attendee_to_event(event_id: UUID, user_id: UUID) -> EventOut:
        event = await Event.find_one(Event.event_id == event_id)
        if not event:
            raise ValueError("Event not found")
        if not any(att.user_id == user_id for att in event.attendees):
            event.attendees.append(UserInteraction(user_id=user_id))
            await event.save()
        return event

    async def add_supporter_to_event(event_id: UUID, user_id: UUID) -> EventOut:
        event = await Event.find_one(Event.event_id == event_id)
        if not event:
            raise ValueError("Event not found")
        if not any(sup.user_id == user_id for sup in event.supporters):
            event.supporters.append(UserInteraction(user_id=user_id))
            await event.save()
        return event

    async def remove_attendee_from_event(event_id: UUID, user_id: UUID) -> EventOut:
        event = await Event.find_one(Event.event_id == event_id)
        if not event:
            raise ValueError("Event not found")
        original_attendees = len(event.attendees)
        event.attendees = [attendee for attendee in event.attendees if attendee.user_id != user_id]
        if len(event.attendees) < original_attendees:
            await event.save()
        return event

    async def remove_supporter_from_event(event_id: UUID, user_id: UUID) -> EventOut:
        event = await Event.find_one(Event.event_id == event_id)
        if not event:
            raise ValueError("Event not found")
        original_supporters = len(event.supporters)
        event.supporters = [supporter for supporter in event.supporters if supporter.user_id != user_id]
        if len(event.supporters) < original_supporters:
            await event.save()
        return event
