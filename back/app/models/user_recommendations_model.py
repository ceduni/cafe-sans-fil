from beanie import Document
from pydantic import BaseModel, Field
from typing import List
from uuid import UUID

"""
This module defines the Pydantic-based models used in the Café application for user recommendations management, 
which are specifically designed for database interaction via the Beanie ODM 
(Object Document Mapper) for MongoDB. These models outline the structure, relationships, 
and constraints of the user-related data stored in the database.

Note: These models are intended for direct database interactions related to users and are 
different from the API data interchange models.
"""

class PersonnalRecommendation(BaseModel):
    cafe_slug: str = Field(..., description="URL-friendly slug for the cafe.")
    recommendation: List[str] = Field(..., description="List of slugs of recommended items in this cafe.")

class UserRecommendation(Document):
    user_id: UUID
    username: str
    personnal_recommendations: List[PersonnalRecommendation]
    cafe_recommendations: List[str]

    class Settings:
        name = "user recommendations"
