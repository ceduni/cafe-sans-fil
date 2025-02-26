"""
Module for handling event-related routes.
"""

from typing import Optional

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Path, Query, Request
from fastapi_pagination.ext.beanie import paginate
from fastapi_pagination.links import Page

from app.auth.dependencies import get_current_user
from app.event.models import EventCreate, EventOut, EventUpdate
from app.event.service import EventService
from app.models import ErrorResponse
from app.service import parse_query_params
from app.user.models import User

event_router = APIRouter()


@event_router.get(
    "/events/",
    response_model=Page[EventOut],
)
async def get_events(
    request: Request,
    cafe_id: Optional[PydanticObjectId] = Query(None, description="Filter by cafe ID."),
    sort_by: Optional[str] = Query(None, description="Sort by a specific field"),
):
    """Get a list of events."""
    filters = parse_query_params(dict(request.query_params))
    events = await EventService.get_all(**filters)
    return await paginate(events)


@event_router.post(
    "/events/",
    response_model=EventOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
)
async def create_event(data: EventCreate):
    """Create an event."""
    return await EventService.create(data)


@event_router.put(
    "/events/{id}",
    response_model=EventOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
)
async def update_event(
    id: PydanticObjectId,
    data: EventUpdate,
):
    """Update an event."""
    event = await EventService.get(id)
    return await EventService.update(event, data)


@event_router.delete(
    "/events/{id}",
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def delete_event(
    id: PydanticObjectId,
):
    """Delete an event."""
    event = await EventService.get(id)
    return await EventService.delete(event)


@event_router.post(
    "/events/{id}/attend",
    responses={
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def toggle_attendance(
    id: PydanticObjectId = Path(..., description="ID of the event"),
    current_user: User = Depends(get_current_user),
    remove: bool = False,
):
    """Toggle attendance for an event."""
    event = await EventService.get(id)
    if not remove:
        return await EventService.add_attendee(event, current_user.id)
    else:
        return await EventService.remove_attendee(event, current_user.id)


@event_router.post(
    "/events/{id}/support",
    responses={
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def toggle_support(
    id: PydanticObjectId = Path(..., description="ID of the event"),
    current_user: User = Depends(get_current_user),
    remove: bool = False,
):
    """Toggle support for an event."""
    event = await EventService.get(id)
    if not remove:
        return await EventService.add_supporter(event, current_user.id)
    else:
        return await EventService.remove_supporter(event, current_user.id)
