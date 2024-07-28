from beanie import Document
from pydantic import BaseModel, Field
from typing import List, Dict
from uuid import UUID

"""
This module defines the Pydantic-based models used in the Café application for user recommendations management, 
which are specifically designed for database interaction via the Beanie ODM 
(Object Document Mapper) for MongoDB. These models outline the structure, relationships, 
and constraints of the user-related data stored in the database.

Note: These models are intended for direct database interactions related to users and are 
different from the API data interchange models.
"""

class Item(BaseModel):
    slug: str = Field(..., description="URL-friendly slug for the menu item.")
    health_score: int = Field(..., description="Health score of the item.")
    cluster: str = Field(..., description="String representing the cluster where the item belongs.")

class CafeForRecommendation(Document):
    slug: str
    health_score: float
    bot_recommendations: List[Item]
    public_recommendations: List[Item]