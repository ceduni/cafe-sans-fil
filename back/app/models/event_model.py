from datetime import datetime
from typing import List, Optional

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, EmailStr, Field


class UserInteraction(BaseModel):
    user_id: PydanticObjectId = Field(..., description="ID of the user who interacted.")
    interaction_time: datetime = Field(
        default_factory=datetime.now, description="The time of the interaction."
    )


class Event(Document):
    cafe_id: PydanticObjectId = Field(
        ..., description="ID of the cafe hosting the event."
    )
    title: str = Field(..., min_length=1, description="Title of the event.")
    description: str = Field(..., description="Detailed description of the event.")
    start_date: datetime = Field(
        ..., description="Starting date and time of the event."
    )
    end_date: Optional[datetime] = Field(
        None, description="Ending date and time of the event, if applicable."
    )
    image_url: Optional[str] = Field(None, description="URL of the event image.")
    attendees: List[UserInteraction] = Field(
        [], description="List of users who have indicated they will attend."
    )
    supporters: List[UserInteraction] = Field(
        [], description="List of users who support the event."
    )

    class Settings:
        name = "events"
