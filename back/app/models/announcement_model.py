from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class UserInteraction(BaseModel):
    user_id: PydanticObjectId = Field(..., description="ID of the user who interacted.")
    interaction_time: datetime = Field(default_factory=datetime.now, description="The time of the interaction.")

class Announcement(Document):
    cafe_id: PydanticObjectId = Field(..., description="ID of the cafe for which the announcement is made.")
    title: str = Field(..., min_length=1, description="Title of the announcement.")
    content: str = Field(..., description="The content of the announcement.")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation date and time of the announcement.")
    active_until: Optional[datetime] = Field(None, description="Date and time until the announcement is considered active.")
    likes: List[UserInteraction] = Field([], description="List of users who have liked the announcement.")
    tags: List[str] = Field([], description="List of tags relevant to the announcement for categorization.")

    class Settings:
        name = "announcements"
