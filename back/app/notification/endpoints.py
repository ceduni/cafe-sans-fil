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
from app.menu.item.service import ItemService
from app.event.service import EventService
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


InteractionPage = CustomizedPage[
    Page[T],
    UseParams(InteractionParams),
]


notification_router = APIRouter()


@notification_router.get("/users/{id}/notifications/{interaction}", response_model=InteractionPage[UserOut])
async def list_notifications(
    request: Request,
    id: PydanticObjectId = Path(..., description="ID of the menu item"),
    interaction: Literal[InteractionType.LIKE, InteractionType.DISLIKE] = Path(
        ..., description="Type of the interaction"
    ),
):
    """Get a list of item interactions."""
    user = await get_current_user(request)
    NotificationService.get_all(
        to_list=True,
    )
    return await paginate(items)

