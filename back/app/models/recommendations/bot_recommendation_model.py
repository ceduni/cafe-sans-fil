from beanie import Document
from typing import List
from pydantic import Field
from app.models.recommendations.item_model import Item

"""
This module defines the Pydantic-based models used in the Café application for bot recommendations management, 
which are specifically designed for database interaction via the Beanie ODM 
(Object Document Mapper) for MongoDB. These models outline the structure, relationships, 
and constraints of the user-related data stored in the database.

Note: These models are intended for direct database interactions related to users and are 
different from the API data interchange models.
"""

class BotRecommendation(Document):
    cafe_slug: str
    recommendation_list: List[Item]

