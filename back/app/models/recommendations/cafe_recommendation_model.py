from beanie import Document, Indexed
from typing import List
from back.app.models.recommendations.cafe_recommendation_model import Cafe
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

"""
This module defines the Pydantic-based models used in the Café application for cafe recommendations management, 
which are specifically designed for database interaction via the Beanie ODM 
(Object Document Mapper) for MongoDB. These models outline the structure, relationships, 
and constraints of the user-related data stored in the database.

Note: These models are intended for direct database interactions related to users and are 
different from the API data interchange models.
"""

class CafeRecommendation(Document):
    user_id: UUID
    recommendation_list: List[Cafe]

class Cafe(BaseModel):
    cafe_id: UUID = Field(default_factory=uuid4)
    slug: Indexed(str, unique=True) = None