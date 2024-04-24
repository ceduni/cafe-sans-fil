from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from typing import List, Optional
from datetime import datetime
from app.models.announcement_model import UserInteraction

class EventCreate(BaseModel):
    title: str = Field(..., min_length=1, description="Title of the event.")
    description: str = Field(..., description="Detailed description of the event.")
    start_date: datetime = Field(..., description="Starting date and time of the event.")
    end_date: Optional[datetime] = Field(None, description="Ending date and time of the event, if applicable.")
    image_url: Optional[str] = Field(None, description="URL of the event image.")
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "title": "Saint-Valentin",
            "description": "Plongez dans l'atmosphère romantique de la Saint-Valentin avec une soirée spécialement conçue pour célébrer l'amour sous toutes ses formes...",
            "start_date": "2025-02-14T10:00:00",
            "end_date": "2026-02-14T14:00:00",
            "image_url": "https://media.istockphoto.com/id/1201265284/vector/happy-valentines-day-handwritten-calligraphic-lettering-with-red-hearts.jpg?s=612x612&w=0&k=20&c=wM-1TL1Y99PLV-fpdd8L3hbG6i3rdoe0KmAFTQHbeTA="
        }
        
    })

class EventOut(BaseModel):
    event_id: UUID = Field(..., description="Unique identifier of the event.")
    cafe_id: UUID = Field(..., description="Identifier of the cafe hosting the event.")
    title: str = Field(..., min_length=1, description="Title of the event.")
    description: str = Field(..., description="Detailed description of the event.")
    start_date: datetime = Field(..., description="Starting date and time of the event.")
    end_date: Optional[datetime] = Field(None, description="Ending date and time of the event, if applicable.")
    image_url: Optional[str] = Field(None, description="URL of the event image.")
    attendees: List[UserInteraction] = Field([], description="List of users who have indicated they will attend.")
    supporters: List[UserInteraction] = Field([], description="List of users who support the event.")
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "event_id": "00000000-0000-0000-0000-000000000000",
            "cafe_id": "00000000-0000-0000-0000-000000000000",
            "title": "Saint-Valentin",
            "description": "Plongez dans l'atmosphère romantique de la Saint-Valentin avec une soirée spécialement conçue pour célébrer l'amour sous toutes ses formes...",
            "start_date": "2025-02-14T10:00:00",
            "end_date": "2026-02-14T14:00:00",
            "image_url": "https://media.istockphoto.com/id/1201265284/vector/happy-valentines-day-handwritten-calligraphic-lettering-with-red-hearts.jpg?s=612x612&w=0&k=20&c=wM-1TL1Y99PLV-fpdd8L3hbG6i3rdoe0KmAFTQHbeTA=",
            "attendees": [],
            "supporters": []
        }
    })
