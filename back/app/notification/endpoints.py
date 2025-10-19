"""
Module for handling notification-related routes.
"""

from typing import List

from fastapi import APIRouter, HTTPException, Path, status

from app.notification.models import (
    NotificationToken,
    SentNotification,
    SendNotificationRequest,
)
from app.notification.service import NotificationService


notification_router = APIRouter()


@notification_router.post(
    "/notifications/register/{expo_token}",
    response_model=NotificationToken,
    status_code=status.HTTP_201_CREATED,
)
async def register_notification_token(
    expo_token: str = Path(..., description="Expo push token to register"),
):
    """Register an Expo push token for notifications."""
    try:
        token = await NotificationService.register_token(expo_token)
        return token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register token: {str(e)}",
        )


@notification_router.post("/notifications/send", status_code=status.HTTP_200_OK)
async def send_notification(request: SendNotificationRequest):
    """Send push notification to all registered devices."""
    result = await NotificationService.send_push_notification(
        title=request.title,
        body=request.body,
    )
    
    if result.get("status") == "error":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("message"),
        )
    
    return result


@notification_router.get(
    "/notifications",
    response_model=List[SentNotification],
    status_code=status.HTTP_200_OK,
)
async def get_notifications():
    """Get all sent notifications."""
    notifications = await NotificationService.get_all_notifications()
    return notifications

