from beanie import Document
from typing import List
from uuid import UUID
from app.models.cafe_recommendations_model import Item

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
    username: str
    personnal_recommendations: List[Item]
    cafe_recommendations: List[str]

    class Settings:
        name = "user recommendations"
