"""
Module for handling event-related routes.
"""

from typing import Optional, TypeVar

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status
from fastapi_pagination import Params
from fastapi_pagination.customization import CustomizedPage, UseParams
from fastapi_pagination.ext.beanie import paginate
from fastapi_pagination.links import Page

from app.auth.dependencies import get_current_user, get_current_user_optional
from app.event.models import EventAggregateOut, EventCreate, EventOut, EventUpdate
from app.event.service import EventService
from app.models import ErrorResponse
from app.service import parse_query_params
from app.user.models import User

T = TypeVar("T")


class EventParams(Params):
    """Custom pagination parameters."""

    size: int = Query(20, ge=1, le=100, description="Page size")
    page: int = Query(1, ge=1, description="Page number")
    sort_by: Optional[str] = Query(None, description="Sort by a specific field")
    cafe_id: Optional[PydanticObjectId] = Query(
        None, description="Filter by cafe ID", example=""
    )


EventPage = CustomizedPage[
    Page[T],
    UseParams(EventParams),
]


event_router = APIRouter()


@event_router.get(
    "/events/",
    response_model=EventPage[EventAggregateOut],
)
async def list_events(
    request: Request,
    current_user: User = Depends(get_current_user_optional),
):
    """Get a list of events."""
    filters = parse_query_params(dict(request.query_params))
    events = await EventService.get_all(
        to_list=False,
        aggregate=True,
        current_user_id=current_user.id if current_user else None,
        **filters,
    )
    return await paginate(events)

@event_router.get(
    "/events/{id}",
    response_model=EventAggregateOut,
)
async def get_event(
    id: PydanticObjectId = Path(..., description="ID of the event"),
    current_user: User = Depends(get_current_user_optional),
):
    """Get an event with full details"""
    event = await EventService.get(
        id,
        aggregate=True,
        current_user_id=current_user.id if current_user else None,
    )
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "An event with this id does not exist"}],
        )
    return event

@event_router.get(
    "/events/@me",
    response_model=EventPage[EventAggregateOut],
)
async def get_events_for_user(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    """Get events created by current user with full details"""
    filters = parse_query_params(dict(request.query_params))
    events = await EventService.get_all_for_user(
        to_list=False,
        aggregate=True,
        current_user_id=current_user.id,
        **filters,
    )
    return await paginate(events)

@event_router.post(
    "/events/",
    response_model=EventOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def create_event(
    data: EventCreate,
    current_user: User = Depends(get_current_user),
):
    """Create an event."""
    # TODO: check perms of user cafes

    return await EventService.create(current_user, data)


@event_router.put(
    "/events/{id}",
    response_model=EventOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def update_event(
    data: EventUpdate,
    id: PydanticObjectId = Path(..., description="ID of the event"),
    current_user: User = Depends(get_current_user),
):
    """Update an event."""
    event = await EventService.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "An event with this ID does not exist."}],
        )

    if event.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=[{"msg": "You are not allowed to update this event."}],
        )

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
    id: PydanticObjectId = Path(..., description="ID of the event"),
    current_user: User = Depends(get_current_user),
):
    """Delete an event."""
    event = await EventService.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "An event with this ID does not exist."}],
        )

    if event.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=[{"msg": "You are not allowed to delete this event."}],
        )

    await EventService.delete(event)
