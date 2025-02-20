from pydantic import BaseModel, Field
from beanie import PydanticObjectId
from typing import List, Optional
from datetime import datetime
from app.models.announcement_model import UserInteraction

class AnnouncementCreate(BaseModel):
    cafe_id: PydanticObjectId = Field(..., description="Identifier of the cafe for which the announcement is made.")
    title: str = Field(..., min_length=1, description="Title of the announcement.")
    content: str = Field(..., description="The content of the announcement.")
    active_until: Optional[datetime] = Field(None, description="Date and time until the announcement is considered active.")
    tags: List[str] = Field([], description="List of tags relevant to the announcement for categorization.")


class AnnouncementUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Title of the announcement.")
    content: Optional[str] = Field(None, description="The content of the announcement.")
    active_until: Optional[datetime] = Field(None, description="Date and time until the announcement is considered active.")
    tags: Optional[List[str]] = Field(None, description="List of tags relevant to the announcement for categorization.")


class AnnouncementOut(BaseModel):
    id: PydanticObjectId = Field(..., description="Unique identifier of the announcement.")
    cafe_id: PydanticObjectId = Field(..., description="Identifier of the cafe for which the announcement is made.")
    title: str = Field(..., min_length=1, description="Title of the announcement.")
    content: str = Field(..., description="The content of the announcement.")
    created_at: datetime = Field(..., description="Creation date and time of the announcement.")
    active_until: Optional[datetime] = Field(None, description="Date and time until the announcement is considered active.")
    likes: List[UserInteraction] = Field([], description="List of users who have liked the announcement.")
    tags: List[str] = Field([], description="List of tags relevant to the announcement for categorization.")
