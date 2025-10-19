"""
Module for handling interaction-related models.
"""

from datetime import UTC, datetime
from typing import Literal, Optional

from beanie import View, PydanticObjectId
from pydantic import BaseModel, Field, HttpUrl
from pymongo import IndexModel

from app.pipeline_builder import PipelineBuilder
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
    read_at: Optional[datetime] = Field(None, description="Timestamp of when the notification was read")
    
    class Settings:
        name = "notification_status"
        is_root = True
        indexes = [
            [("user_id", 1), ("message_id", 1)]
        ]
        
        
        
class UserNotificationPipelineBuilder(PipelineBuilder):
    def __init__(self, model):
        super().__init__(
            model=model,
            root_fields={"user_id", "message_id", "read", "delivered_at", "read_at"},
            lookup_from="notification_messages",
            local_field="message_id",
            joined_prefix="message"
        )
        
class UserNotification(View):
    """Aggregated notification for a specific user."""

    user_id: PydanticObjectId
    message_id: PydanticObjectId
    title: str
    message: str
    type: NotificationType
    action: Optional[Action]
    created_at: datetime
    read: bool
    delivered_at: datetime
    read_at: Optional[datetime]
        
    class Settings:
        name: str = "user_notifications_view"
        source = "notification_status"
        is_view = True
        @classmethod
        def pipeline(cls):
            return UserNotificationPipelineBuilder(cls).build_pipeline()
        # pipeline = UserNotificationPipelineBuilder().build_pipeline()
        # pipeline = [
        #     {
        #         "$lookup": {
        #             "from": "notification_messages",
        #             "localField": "message_id",
        #             "foreignField": "_id",
        #             "as": "message"
        #         }
        #     },
        #     {
        #         "$project": {
        #             "user_id": 1,
        #             "read": 1,
        #             "delivered_at": 1,
        #             "message_id": "$message._id",
        #             "title": "$message.title",
        #             "message": "$message.message",
        #             "type": "$message.type",
        #             "action": "$message.action",
        #             "created_at": "$message.created_at",
        #             "read_at": "$message.read_at"
        #         }
        #     },
        # ]
