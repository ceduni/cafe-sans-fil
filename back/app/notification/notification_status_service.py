"""
Module for handling interaction-related operations.
"""

from typing import Any, Dict, List, Union, Optional
from beanie import PydanticObjectId

from app.notification.models import NotificationStatus


class NotificationStatusService:
    """Service for handling interaction-related operations."""


    @staticmethod
    async def get_all(user_id:str, to_list: bool = True,**filters: dict) -> Union[List[NotificationStatus], Any]:
        """Get user notifications."""
        
        try:
            filters["user_id"] = PydanticObjectId(user_id)
        except Exception as e:
            raise ValueError(f"Invalid user_id: {user_id}") from e
    
        query = NotificationStatus.find(filters)
        
        return await query.to_list() if to_list else query
    
    
    @staticmethod
    async def get_by_id(notification_id: str) -> Optional[NotificationStatus]:
        """Retrieve a notification by its ID."""
        try:
            return await NotificationStatus.get(PydanticObjectId(notification_id))
        except Exception:
            return None
    
    
    @staticmethod
    async def create(user_id: str, msg_id: str) -> NotificationStatus:
        status = NotificationStatus(
            user_id=PydanticObjectId(user_id),
            message_id=PydanticObjectId(msg_id),
        )
        return await status.insert()      

    @staticmethod
    async def delete(user_id: str, msg_id: str) -> bool:
        """Delete an interaction."""
        notification = await NotificationStatusService.get_notification(user_id, msg_id)
        if not notification:
            return False

        await notification.delete()
        return True
    
    
    @staticmethod
    async def mark_as_read(user_id: str, msg_id: str) -> Optional[NotificationStatus]:
        status = await NotificationStatusService.get_notification(user_id, msg_id)
        if not status:
            return None
        status.read = True
        return await status.save()



    ## Helpers method
  
    @staticmethod
    async def get_notification(user_id:str, message_id:str)->dict:
        return await NotificationStatus.find_one(NotificationStatusService.buildKey(user_id, message_id))
  
    @staticmethod
    def buildKey(user_id:str, message_id:str)->dict:
        return {
            "user_id": PydanticObjectId(user_id),
            "message_id": PydanticObjectId(message_id)
        }