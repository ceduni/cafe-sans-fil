"""
Module for handling interaction-related models.
"""

from datetime import UTC, datetime
from typing import Literal, Optional

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field, HttpUrl
from pymongo import IndexModel

from app.models import CustomDocument, UserId
from app.notification.enums import NotificationType, ActionType

class Action(BaseModel):
    type: ActionType = ActionType.LINK
    label: str = Field(..., description="Button label or action name")
    link: Optional[HttpUrl] = Field(None, description="URL to open if type is 'link'")


class NotificationMessage(CustomDocument):
    """Model for notification messages."""

    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    title: str = Field(..., description="Notification title")
    message: str = Field(..., description="Notification message")
    type: NotificationType = Field(NotificationType.INFO, description="Type of the notification")
    action: Optional[Action] = Field(None, description="Optional action to take")
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(UTC))

    class Settings:
        """Settings for interaction document."""

        name = "notification_messages"
        is_root = True


class NotificationStatus(CustomDocument, UserId):
    """Model for notification status."""

    message_id: PydanticObjectId = Field(..., description="Reference to the NotificationMessage")
    read: bool = Field(default=False, description="Indicates if the notification has been read")
    delivered_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    
    class Settings:
        name = "notification_status"
        is_root = True
        
class UserNotification(BaseModel):
    """Aggregated notification for a specific user."""

    id: PydanticObjectId
    title: str
    message: str
    type: NotificationType
    action: Optional[Action]
    created_at: datetime

    read: bool
    delivered_at: datetime

    class Config:
        orm_mode = True


class NotificationToken(CustomDocument):
    """Model for storing Expo push tokens."""

    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    expo_token: str = Field(..., description="Expo push token", unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Settings:
        """Settings for notification token document."""
        name = "notification_ids"
        is_root = True
        indexes = [
            IndexModel("expo_token", unique=True),
        ]


class SentNotification(CustomDocument):
    """Model for storing sent push notifications."""

    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    title: str = Field(..., description="Notification title")
    body: str = Field(..., description="Notification body")
    sent_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Settings:
        """Settings for sent notification document."""
        name = "notifs"
        is_root = True


class SendNotificationRequest(BaseModel):
    """Request model for sending notifications."""
    title: str = Field(..., description="Notification title")
    body: str = Field(..., description="Notification body") 