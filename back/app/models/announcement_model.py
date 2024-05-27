from beanie import Document
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID, uuid4

class UserInteraction(BaseModel):
    user_id: UUID = Field(..., description="The id of the user who interacted.")
    interaction_time: datetime = Field(default_factory=datetime.now, description="The time of the interaction.")

class Announcement(Document):
    announcement_id: UUID = Field(default_factory=uuid4, description="Unique identifier of the announcement.")
    cafe_id: UUID = Field(..., description="Identifier of the cafe for which the announcement is made.")
    title: str = Field(..., min_length=1, description="Title of the announcement.")
    content: str = Field(..., description="The content of the announcement.")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation date and time of the announcement.")
    active_until: Optional[datetime] = Field(None, description="Date and time until the announcement is considered active.")
    likes: List[UserInteraction] = Field([], description="List of users who have liked the announcement.")
    tags: List[str] = Field([], description="List of tags relevant to the announcement for categorization.")

    class Settings:
        name = "announcements"
