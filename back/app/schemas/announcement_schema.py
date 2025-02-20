from pydantic import BaseModel, Field, ConfigDict
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
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "cafe_id": "67b600414ae53a72130a956e",
            "title": "Distribution de Chocolat Gratuit",
            "content": "Pour égayer votre journée, passez au Café Étudiant ce mercredi! Nous distribuons des chocolats gratuits pour tous nos visiteurs. Une petite douceur pour accompagner vos études et vos pauses café",
            "active_until": "2025-12-31T23:59:59",
            "tags": ["Rapide", "Chocalat"]
        }
    })

class AnnouncementUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Title of the announcement.")
    content: Optional[str] = Field(None, description="The content of the announcement.")
    active_until: Optional[datetime] = Field(None, description="Date and time until the announcement is considered active.")
    tags: Optional[List[str]] = Field(None, description="List of tags relevant to the announcement for categorization.")
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "title": "Distribution de Chocolat Gratuit",
            "content": "Pour égayer votre journée, passez au Café Étudiant ce mercredi! Nous distribuons des chocolats gratuits pour tous nos visiteurs. Une petite douceur pour accompagner vos études et vos pauses café",
            "active_until": "2025-12-31T23:59:59",
            "tags": ["Rapide", "Chocalat"]
        }
    })

class AnnouncementOut(BaseModel):
    id: PydanticObjectId = Field(..., description="Unique identifier of the announcement.")
    cafe_id: PydanticObjectId = Field(..., description="Identifier of the cafe for which the announcement is made.")
    title: str = Field(..., min_length=1, description="Title of the announcement.")
    content: str = Field(..., description="The content of the announcement.")
    created_at: datetime = Field(..., description="Creation date and time of the announcement.")
    active_until: Optional[datetime] = Field(None, description="Date and time until the announcement is considered active.")
    likes: List[UserInteraction] = Field([], description="List of users who have liked the announcement.")
    tags: List[str] = Field([], description="List of tags relevant to the announcement for categorization.")
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": "67b600414ae53a72130a956e",
            "cafe_id": "67b600414ae53a72130a956a",
            "title": "Distribution de Chocolat Gratuit",
            "content": "Pour égayer votre journée, passez au Café Étudiant ce mercredi! Nous distribuons des chocolats gratuits pour tous nos visiteurs. Une petite douceur pour accompagner vos études et vos pauses café",
            "created_at": "2022-01-01T00:00:00",
            "active_until": "2025-12-31T23:59:59",
            "likes": [],
            "tags": ["Rapide", "Chocalat"]
        }
    })
