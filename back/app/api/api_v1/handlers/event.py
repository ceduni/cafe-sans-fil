from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import UUID

from app.schemas.event_schema import EventCreate, EventOut
from app.services.event_service import create_event, get_events

event_router = APIRouter()

@event_router.get("/events/", response_model=List[EventOut])
async def list_events_handler():
    return await get_events()

@event_router.post("/events/", response_model=EventOut)
async def create_event_handler(event: EventCreate):
    return await create_event(event)

