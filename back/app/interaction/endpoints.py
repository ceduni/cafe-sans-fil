"""
Module for handling interaction-related routes.
"""

from typing import Literal, Optional, TypeVar

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status
from fastapi_pagination import Params
from fastapi_pagination.customization import CustomizedPage, UseParams
from fastapi_pagination.ext.beanie import paginate
from fastapi_pagination.links import Page

from app.auth.dependencies import get_current_user
from app.cafe.announcement.service import AnnouncementService
from app.cafe.event.service import EventService
from app.cafe.menu.item.service import ItemService
from app.interaction.enums import InteractionType
from app.interaction.service import InteractionService
from app.models import ErrorResponse
from app.service import parse_query_params
from app.user.models import UserOut

T = TypeVar("T")


class InteractionParams(Params):
    """Custom pagination parameters."""

    size: int = Query(20, ge=1, le=100, description="Page size")
    page: int = Query(1, ge=1, description="Page number")
    sort_by: Optional[str] = Query(None, description="Sort by a specific field")


InteractionPage = CustomizedPage[
    Page[T],
    UseParams(InteractionParams),
]


interaction_router = APIRouter()


@interaction_router.get(
    "/items/{id}/interactions/{interaction}",
    response_model=InteractionPage[UserOut],
)
async def get_item_interactions(
    request: Request,
    id: PydanticObjectId = Path(..., description="ID of the menu item"),
    interaction: Literal[InteractionType.LIKE, InteractionType.DISLIKE] = Path(
        ..., description="Type of the interaction"
    ),
):
    """Get a list of item interactions."""
    item = await ItemService.get(id=id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "An item with this ID does not exist."}],
        )

    filters = parse_query_params(dict(request.query_params))
    filters["item_id"] = item.id
    filters["type"] = interaction

    items = await InteractionService.get_all(to_list=False, **filters)

    return await paginate(items)


@interaction_router.get(
    "/announcements/{id}/interactions/{interaction}",
    response_model=InteractionPage[UserOut],
)
async def get_announcement_interactions(
    request: Request,
    id: PydanticObjectId = Path(..., description="ID of the announcement"),
    interaction: Literal[InteractionType.LIKE, InteractionType.DISLIKE] = Path(
        ..., description="Type of the interaction"
    ),
):
    """Get a list of announcement interactions."""
    announcement = await AnnouncementService.get(id=id)
    if not announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "An announcement with this ID does not exist."}],
        )

    filters = parse_query_params(dict(request.query_params))
    filters["announcement_id"] = id
    filters["type"] = interaction

    announcement = await InteractionService.get_all(to_list=False, **filters)

    return await paginate(announcement)


@interaction_router.get(
    "/events/{id}/interactions/{interaction}",
    response_model=InteractionPage[UserOut],
)
async def get_event_interactions(
    request: Request,
    id: PydanticObjectId = Path(..., description="ID of the event"),
    interaction: InteractionType = Path(..., description="Type of the interaction"),
):
    """Get a list of event interactions."""
    event = await EventService.get(id=id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "An event with this ID does not exist."}],
        )

    filters = parse_query_params(dict(request.query_params))
    filters["event_id"] = id
    filters["type"] = interaction

    events = await InteractionService.get_all(to_list=False, **filters)

    return await paginate(events)


@interaction_router.post(
    "/items/{id}/interactions/{interaction}/@me",
    responses={
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def create_item_interaction(
    id: PydanticObjectId = Path(..., description="ID of the menu item"),
    interaction: Literal[InteractionType.LIKE, InteractionType.DISLIKE] = Path(
        ..., description="Type of the interaction"
    ),
    current_user: dict = Depends(get_current_user),
):
    """Create an interaction for a menu item. (`MEMBER`)"""
    item = await ItemService.get(id=id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "An item with this ID does not exist."}],
        )

    if await InteractionService.get(
        user=current_user,
        type=interaction,
        item=item,
    ):
        return

    await InteractionService.create(
        user=current_user,
        type=interaction,
        item=item,
    )


@interaction_router.post(
    "/announcements/{id}/interactions/{interaction}/@me",
    responses={
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def create_announcement_interaction(
    id: PydanticObjectId = Path(..., description="ID of the announcement"),
    interaction: Literal[InteractionType.LIKE, InteractionType.DISLIKE] = Path(
        ..., description="Type of the interaction"
    ),
    current_user: dict = Depends(get_current_user),
):
    """Create an interaction for an announcement. (`MEMBER`)"""
    announcement = await AnnouncementService.get(id=id)
    if not announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "An announcement with this ID does not exist."}],
        )

    if await InteractionService.get(
        user=current_user,
        type=interaction,
        announcement=announcement,
    ):
        return

    await InteractionService.create(
        user=current_user,
        type=interaction,
        announcement=announcement,
    )


@interaction_router.post(
    "/events/{id}/interactions/{interaction}/@me",
    responses={
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def create_event_interaction(
    id: PydanticObjectId = Path(..., description="ID of the event"),
    interaction: InteractionType = Path(..., description="Type of the interaction"),
    current_user: dict = Depends(get_current_user),
):
    """Create an interaction for an event. (`MEMBER`)"""
    event = await EventService.get(id=id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "An event with this ID does not exist."}],
        )

    if await InteractionService.get(
        user=current_user,
        type=interaction,
        event=event,
    ):
        return

    await InteractionService.create(
        user=current_user,
        type=interaction,
        event=event,
    )


@interaction_router.delete(
    "/items/{id}/interactions/{interaction}/@me",
    responses={
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def delete_item_interaction(
    id: PydanticObjectId = Path(..., description="ID of the menu item"),
    interaction: Literal[InteractionType.LIKE, InteractionType.DISLIKE] = Path(
        ..., description="Type of the interaction"
    ),
    current_user: dict = Depends(get_current_user),
):
    """Delete an interaction for a menu item. (`MEMBER`)"""
    item = await ItemService.get(id=id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "An item with this ID does not exist."}],
        )

    interaction = await InteractionService.get(
        user=current_user,
        type=interaction,
        item=item,
    )

    if not interaction:
        return

    await InteractionService.delete(interaction)


@interaction_router.delete(
    "/announcements/{id}/interactions/{interaction}/@me",
    responses={
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def delete_announcement_interaction(
    id: PydanticObjectId = Path(..., description="ID of the announcement"),
    interaction: Literal[InteractionType.LIKE, InteractionType.DISLIKE] = Path(
        ..., description="Type of the interaction"
    ),
    current_user: dict = Depends(get_current_user),
):
    """Delete an interaction for an announcement. (`MEMBER`)"""
    announcement = await AnnouncementService.get(id=id)
    if not announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "An announcement with this ID does not exist."}],
        )

    interaction = await InteractionService.get(
        user=current_user,
        type=interaction,
        announcement=announcement,
    )

    if not interaction:
        return

    await InteractionService.delete(interaction)


@interaction_router.delete(
    "/events/{id}/interactions/{interaction}/@me",
    responses={
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def delete_event_interaction(
    id: PydanticObjectId = Path(..., description="ID of the event"),
    interaction: InteractionType = Path(..., description="Type of the interaction"),
    current_user: dict = Depends(get_current_user),
):
    """Delete an interaction for an event. (`MEMBER`)"""
    event = await EventService.get(id=id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "An event with this ID does not exist."}],
        )

    interaction = await InteractionService.get(
        user=current_user,
        type=interaction,
        event=event,
    )

    if not interaction:
        return

    await InteractionService.delete(interaction)
