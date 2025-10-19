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
from app.notification.models import UserNotification
from app.notification.notification_message_service import NotificationMessageService
from app.notification.notification_status_service import NotificationStatusService
from app.notification.user_notification_service import UserNotificationService
from app.service import parse_query_params
from app.user.models import User

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

@notification_router.get("/notifications/", response_model=InteractionPage[UserNotification])
async def list_user_notifications(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    """Get a list of notifications for the current user."""
    filters = parse_query_params(dict(request.query_params))
    notifications = UserNotificationService.get_all(
        user_id=current_user.id if current_user else None,
        to_list=True,
        **filters,
    )
    
    return await paginate(notifications)

@notification_router.get("/notifications/{id}", response_model=InteractionPage[UserNotification])
async def get_user_notification(
    current_user: User = Depends(get_current_user),
    id: PydanticObjectId = Path(..., description="ID of the notification")
):
    """Get a list of notifications for the current user."""
    notification = UserNotificationService.get_by_id(
        current_user,
        id,
    )
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A notification with this id does not exist"}],
        )
        
    return await notification

