from beanie import Document
from typing import List
from pydantic import BaseModel, Field
from uuid import UUID

"""
This module defines the Pydantic-based models used in the Café application for cafe recommendations management, 
which are specifically designed for database interaction via the Beanie ODM 
(Object Document Mapper) for MongoDB. These models outline the structure, relationships, 
and constraints of the user-related data stored in the database.

Note: These models are intended for direct database interactions related to users and are 
different from the API data interchange models.
"""

class Cafe(BaseModel):
    slug: str = Field(None, description="Slug d'un café.")
    score: float

class CafeRecommendation(Document):
    user_id: UUID
    recommendation_list: List[Cafe]