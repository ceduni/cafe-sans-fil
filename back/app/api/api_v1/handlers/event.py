from fastapi import APIRouter, HTTPException, Depends, Path
from typing import List
from uuid import UUID

from app.schemas.event_schema import EventCreate, EventOut
from app.services.event_service import EventService
from app.models.user_model import User
from app.api.deps.user_deps import get_current_user

event_router = APIRouter()

@event_router.get("/events/", response_model=List[EventOut])
async def list_events():
    return await EventService.get_events()

@event_router.post("/events/", response_model=EventOut)
async def create_event(event: EventCreate):
    return await EventService.create_event(event)

@event_router.delete("/events/{event_id}")
async def delete_event(event_id: UUID):
    return await EventService.remove_event(event_id)

@event_router.post("/events/{event_id}/attend", response_model=EventOut)
async def toggle_attendance(
    event_id: UUID = Path(..., description="The ID of the event"),
    current_user: User = Depends(get_current_user),
    remove: bool = False
):
    if not remove:
        return await EventService.add_attendee_to_event(event_id, current_user.user_id)
    else:
        return await EventService.remove_attendee_from_event(event_id, current_user.user_id)

@event_router.post("/events/{event_id}/support", response_model=EventOut)
async def toggle_support(
    event_id: UUID = Path(..., description="The ID of the event"),
    current_user: User = Depends(get_current_user),
    remove: bool = False
):
    if not remove:
        return await EventService.add_supporter_to_event(event_id, current_user.user_id)
    else:
        return await EventService.remove_supporter_from_event(event_id, current_user.user_id)