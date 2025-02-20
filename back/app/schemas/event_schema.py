from datetime import datetime
from typing import List, Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from app.models.announcement_model import UserInteraction


class EventCreate(BaseModel):
    cafe_id: PydanticObjectId
    title: str = Field(..., min_length=1)
    description: str
    start_date: datetime
    end_date: Optional[datetime] = None
    image_url: Optional[str] = None


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    image_url: Optional[str] = None


class EventOut(BaseModel):
    id: PydanticObjectId
    cafe_id: PydanticObjectId
    title: str = Field(..., min_length=1)
    description: str
    start_date: datetime
    end_date: Optional[datetime] = None
    image_url: Optional[str] = None
    attendees: List[UserInteraction] = []
    supporters: List[UserInteraction] = []
