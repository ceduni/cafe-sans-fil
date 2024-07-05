from pydantic import ConfigDict, BaseModel, Field
from uuid import UUID
from typing import List, Dict, Optional

"""
This module defines the Pydantic-based schemas for user recommendations. 
These schemas are utilized for request and response validation, serialization, 
and documentation specific to user item recommendations.

Note: These models are for API data interchange related to users and not direct database models.
"""

# ----------------------------------------------
#               Cafe
# ----------------------------------------------

class CafeOut(BaseModel):
    slug: str = Field(None, description="URL-friendly slug for the cafe.")
    model_config = ConfigDict(json_schema_extra={
        "slug": "tore-et-fraction"
    })

# ----------------------------------------------
#               Item
# ----------------------------------------------

class ItemOut(BaseModel):
    slug: str = Field(None, description="URL-friendly slug for the menu item.")
    health_score: int = Field(None, description="Health score of the item.")
    cluster: str = Field(..., description="String representing the cluster where the item belongs.")
    model_config = ConfigDict(json_schema_extra={
        "slug": "cheeseburger",
        "health_score": 5,
        "cluster": "0"
    })

class ItemUpdate(BaseModel):
    slug: Optional[str] = Field(None, description="URL-friendly slug for the menu item.")
    health_score: Optional[int] = Field(None, description="Health score of the item.")
    cluster: Optional[str] = Field(..., description="String representing the cluster where the item belongs.")
    model_config = ConfigDict(json_schema_extra={
        "slug": "cheeseburger",
        "health_score": 5,
        "cluster": "0"
    })


# ----------------------------------------------
#               Recommendations
# ----------------------------------------------

class ItemRecommendationOut(BaseModel):
    recommendations: List[str] = Field(..., description="Recommendations for each cafe.")
    model_config = ConfigDict(json_schema_extra={
        "exemple": {
            "recommendations":  ['cheeseburger', "Cheeseburger Spécial"]
        }
    })

class ItemRecommendationUpdate(BaseModel):
    recommendations: Optional[List[str]] = Field(..., description="Recommendations for each cafe.")
    model_config = ConfigDict(json_schema_extra={
        "exemple": {
            "recommendations":  ["cheeseburger", "Cheeseburger Spécial"]
        }
    })

class CafeRecommendationOut(BaseModel):
    user_id: UUID = Field(..., description="id of the user receiving the recommendations.")
    recommendations: List[str] = Field(..., description="List of cafe slugs recommended to the user.")
    model_config = ConfigDict(json_schema_extra={
        "exemple": {
            "user_id": "4bd4d340-e2b0-404f-a8b6-7af8eef33411",
            "recommendations": ["tore-et-fraction"]
        }
    })

class CafeRecommendationUpdate(BaseModel):
    user_id: Optional[UUID] = Field(..., description="id of the user receiving the recommendations.")
    recommendations: Optional[List[str]] = Field(..., description="List of cafe slugs recommended to the user.")
    model_config = ConfigDict(json_schema_extra={
        "exemple": {
            "user_id": "4bd4d340-e2b0-404f-a8b6-7af8eef33411",
            "recommendations": ["tore-et-fraction"]
        }
    })