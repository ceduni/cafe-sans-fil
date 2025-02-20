from datetime import datetime
from typing import List, Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from app.models.announcement_model import UserInteraction


class EventCreate(BaseModel):
    cafe_id: PydanticObjectId = Field(
        ..., description="Identifier of the cafe hosting the event."
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


class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Title of the event.")
    description: Optional[str] = Field(
        None, description="Detailed description of the event."
    )
    start_date: Optional[datetime] = Field(
        None, description="Starting date and time of the event."
    )
    end_date: Optional[datetime] = Field(
        None, description="Ending date and time of the event, if applicable."
    )
    image_url: Optional[str] = Field(None, description="URL of the event image.")


class EventOut(BaseModel):
    id: PydanticObjectId = Field(..., description="Unique identifier of the event.")
    cafe_id: PydanticObjectId = Field(
        ..., description="Identifier of the cafe hosting the event."
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
