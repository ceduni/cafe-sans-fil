from pydantic import BaseModel, Field

"""
This module defines the Pydantic-based models used in the Café application for public recommendations management, 
which are specifically designed for database interaction via the Beanie ODM 
(Object Document Mapper) for MongoDB. These models outline the structure, relationships, 
and constraints of the user-related data stored in the database.

Note: These models are intended for direct database interactions related to users and are 
different from the API data interchange models.
"""

class Item(BaseModel):
    slug: str = Field(None, description="URL-friendly slug for the menu item.")
    health_score: int = Field(None, description="Health score of the item.")
    cluster: str = Field(..., description="String representing the cluster where the item belongs.")