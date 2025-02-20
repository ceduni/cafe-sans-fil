from datetime import datetime
from typing import List, Optional

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, EmailStr, Field


class UserInteraction(BaseModel):
    user_id: PydanticObjectId
    interaction_time: datetime = Field(default_factory=datetime.now)


class Event(Document):
    cafe_id: PydanticObjectId
    title: str = Field(..., min_length=1)
    description: str
    start_date: datetime
    end_date: Optional[datetime] = None
    image_url: Optional[str] = None
    attendees: List[UserInteraction] = []
    supporters: List[UserInteraction] = []

    class Settings:
        name = "events"
