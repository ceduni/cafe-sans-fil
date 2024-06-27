from beanie import Document, Indexed, DecimalAnnotation
from typing import List
from back.app.models.user_recommendation_model import Item
from pydantic import field_validator, BaseModel, Field
from uuid import UUID

"""
This module defines the Pydantic-based models used in the Café application for user recommendations management, 
which are specifically designed for database interaction via the Beanie ODM 
(Object Document Mapper) for MongoDB. These models outline the structure, relationships, 
and constraints of the user-related data stored in the database.

Note: These models are intended for direct database interactions related to users and are 
different from the API data interchange models.
"""

class UserRecommendation(Document):
    user_id: UUID
    cafe_slug: str
    recommendation_list: List[Item]

class Item(BaseModel):
    slug: Indexed(str, unique=True) = Field(None, description="URL-friendly slug for the menu item.")
    item_id: UUID = Field(default_factory=uuid4, description="Unique identifier of the menu item.")
    