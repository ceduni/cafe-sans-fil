"""
Module for handling event-related routes.
"""

from typing import Dict, List, Optional

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request

from app.auth.dependencies import get_current_user
from app.event.models import EventCreate, EventOut, EventUpdate
from app.event.service import EventService
from app.service import parse_query_params
from app.user.models import User

event_router = APIRouter()


@event_router.get(
    "/events/",
    response_model=List[EventOut],
)
async def get_events(
    request: Request,
    cafe_id: Optional[PydanticObjectId] = Query(
        None, description="Filter events by cafe ID."
    ),
    sort_by: Optional[str] = Query(
        "-start_date",
        description="Sort events by a specific field. Prefix with '-' for descending order (e.g., '-start_date').",
    ),
    page: Optional[int] = Query(
        1, description="Specify the page number for pagination."
    ),
    limit: Optional[int] = Query(
        9, description="Set the number of events to return per page."
    ),
) -> List[EventOut]:
    """Get a list of events."""
    query_params = dict(request.query_params)
    parsed_params = parse_query_params(query_params)
    return await EventService.get_events(**parsed_params)


@event_router.post(
    "/events/",
    response_model=EventOut,
)
async def create_event(event: EventCreate) -> EventOut:
    """Create an event."""
    return await EventService.create_event(event)


@event_router.put(
    "/events/{event_id}",
    response_model=EventOut,
)
async def update_event(event_id: PydanticObjectId, event: EventUpdate) -> EventOut:
    """Update an event."""
    return await EventService.update_event(event_id, event)


@event_router.delete(
    "/events/{event_id}",
)
async def delete_event(event_id: PydanticObjectId):
    """Delete an event."""
    return await EventService.remove_event(event_id)


@event_router.post(
    "/events/{event_id}/attend",
    response_model=EventOut,
)
async def toggle_attendance(
    event_id: PydanticObjectId = Path(..., description="The ID of the event"),
    current_user: User = Depends(get_current_user),
    remove: bool = False,
):
    """Toggle attendance for an event."""
    if not remove:
        return await EventService.add_attendee_to_event(event_id, current_user.id)
    else:
        return await EventService.remove_attendee_from_event(event_id, current_user.id)


@event_router.post(
    "/events/{event_id}/support",
    response_model=EventOut,
)
async def toggle_support(
    event_id: PydanticObjectId = Path(..., description="The ID of the event"),
    current_user: User = Depends(get_current_user),
    remove: bool = False,
):
    """Toggle support for an event."""
    if not remove:
        return await EventService.add_supporter_to_event(event_id, current_user.id)
    else:
        return await EventService.remove_supporter_from_event(event_id, current_user.id)
