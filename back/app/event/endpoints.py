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

from app.cafe.permissions import AdminPermission
from app.cafe.service import CafeService
from app.event.models import EventCreate, EventOut, EventUpdate, EventViewOut
from app.event.service import EventService
from app.models import ErrorResponse
from app.service import parse_query_params
from app.user.endpoints import get_current_user
from app.user.models import User

T = TypeVar("T")


class EventParams(Params):
    """Custom pagination parameters."""

    size: int = Query(20, ge=1, le=100, description="Page size")
    page: int = Query(1, ge=1, description="Page number")
    sort_by: Optional[str] = Query(None, description="Sort by a specific field")
    cafe_id: Optional[PydanticObjectId] = Query(None, description="Filter by cafe ID.")


EventPage = CustomizedPage[
    Page[T],
    UseParams(EventParams),
]


event_router = APIRouter()


@event_router.get(
    "/events/",
    response_model=EventPage[EventViewOut],
)
async def get_events(
    request: Request,
):
    """Get a list of events."""
    filters = parse_query_params(dict(request.query_params))
    events = await EventService.get_all(to_list=False, as_view=True, **filters)
    return await paginate(events)


@event_router.post(
    "/cafes/{slug}/events/",
    response_model=EventOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
    dependencies=[Depends(AdminPermission())],
)
async def create_event(
    data: EventCreate,
    slug: str = Path(..., description="Slug of the cafe"),
    current_user: User = Depends(get_current_user),
):
    """Create an event. (`ADMIN`)"""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    return await EventService.create(current_user, cafe, data)


@event_router.put(
    "/cafes/{slug}/events/{id}",
    response_model=EventOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
    dependencies=[Depends(AdminPermission())],
)
async def update_event(
    data: EventUpdate,
    slug: str = Path(..., description="Slug of the cafe"),
    id: PydanticObjectId = Path(..., description="ID of the event"),
):
    """Update an event. (`ADMIN`)"""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    event = await EventService.get_by_id_and_cafe_id(id, cafe.id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "An event with this ID does not exist."}],
        )

    return await EventService.update(event, data)


@event_router.delete(
    "/cafes/{slug}/events/{id}",
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
    dependencies=[Depends(AdminPermission())],
)
async def delete_event(
    slug: str = Path(..., description="Slug of the cafe"),
    id: PydanticObjectId = Path(..., description="ID of the event"),
):
    """Delete an event. (`ADMIN`)"""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    event = await EventService.get_by_id_and_cafe_id(id, cafe.id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "An event with this ID does not exist."}],
        )

    await EventService.delete(event)
