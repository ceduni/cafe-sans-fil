from typing import List
from app.models.event_model import Event
from app.schemas.event_schema import EventCreate, EventOut

async def get_events() -> List[EventOut]:
    return await Event.find_all().to_list()

async def create_event(event_data: EventCreate) -> EventOut:
    event = Event(**event_data.model_dump())
    await event.insert()
    return event