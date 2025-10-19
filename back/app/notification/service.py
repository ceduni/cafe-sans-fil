"""
Module for handling interaction-related operations.
"""

from typing import Any, Dict, List, Union
import httpx

from beanie import PydanticObjectId
from beanie.odm.queries.find import AggregationQuery

from app.notification.models import (
    NotificationType,
    NotificationToken,
    SentNotification,
)
from app.user.models import User


class NotificationService:
    """Service for handling notification-related operations."""

    @staticmethod
    async def register_token(expo_token: str) -> NotificationToken:
        """Register or update an Expo push token."""
        existing_token = await NotificationToken.find_one(NotificationToken.expo_token == expo_token)
        if existing_token:
            return existing_token
        
        token = NotificationToken(expo_token=expo_token)
        await token.insert()
        return token

    @staticmethod
    async def send_push_notification(title: str, body: str) -> Dict[str, Any]:
        """Send push notification to all registered tokens."""
        # Get all registered tokens
        tokens = await NotificationToken.find_all().to_list()
        
        if not tokens:
            return {"status": "error", "message": "No registered tokens found"}
        
        # Prepare the list of Expo tokens
        expo_tokens = [token.expo_token for token in tokens]
        
        # Prepare the payload for Expo push notification
        payload = {
            "to": expo_tokens,
            "title": title,
            "body": body,
        }
        
        # Send the notification via Expo API
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    "https://exp.host/--/api/v2/push/send",
                    json=payload,
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    timeout=10.0
                )
                response.raise_for_status()
                result = response.json()
                
                # Store the notification in the database
                sent_notif = SentNotification(title=title, body=body)
                await sent_notif.insert()
                
                return {
                    "status": "success",
                    "expo_response": result,
                    "notification_id": str(sent_notif.id)
                }
            except httpx.HTTPError as e:
                return {
                    "status": "error",
                    "message": f"Failed to send notification: {str(e)}"
                }

    @staticmethod
    async def get_all_notifications() -> List[SentNotification]:
        """Get all sent notifications."""
        return await SentNotification.find_all().sort(-SentNotification.sent_at).to_list()
  