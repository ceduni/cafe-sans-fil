from pydantic import ConfigDict, BaseModel, Field
from typing import List, Optional, Dict
from uuid import UUID

"""
This module defines the Pydantic-based schemas for user recommendations. 
These schemas are utilized for request and response validation, serialization, 
and documentation specific to user item recommendations.

Note: These models are for API data interchange related to users and not direct database models.
"""

# ----------------------------------------------
#               Item
# ----------------------------------------------

class ItemOut(BaseModel):
    item_id: UUID = Field(..., description="Unique identifier for the item.")
    slug: str = Field(..., description="URL-friendly slug for the menu item.")
    health_score: int = Field(..., description="Health score of the item.")
    cluster: str = Field(..., description="String representing the cluster where the item belongs.")
    model_config = ConfigDict(json_schema_extra={
        "exemple": {
            "item_id": "123e4567-e89b-12d3-a456-426614174000",
            "slug": "cheeseburger",
            "health_score": 5,
            "cluster": "0"
        }
    })

class ItemUpdate(BaseModel):
    slug: Optional[str] = Field(None, description="URL-friendly slug for the menu item.")
    health_score: Optional[int] = Field(None, description="Health score of the item.")
    cluster: Optional[str] = Field(None, description="String representing the cluster where the item belongs.")
    model_config = ConfigDict(json_schema_extra={
        "exemple": {
            "slug": "cheeseburger",
            "health_score": 5,
            "cluster": "0"
        }
    })

# ----------------------------------------------
#               Cafe
# ----------------------------------------------

class CafeOut(BaseModel):
    slug: str = Field(..., description="URL-friendly slug for the cafe.")
    health_score: float = Field(..., description="Score of the cafe.")
    public_recommendations: List[str] = Field(..., description="List of recommended items in this cafe.")
    model_config = ConfigDict(json_schema_extra={
        "exemple": {
            "slug": "tore-et-fraction",
            "health_score": 5,
            "public_recommendations": [
                "cheeseburger",
            ]
        }
    })

class CafeShortOut(BaseModel):
    slug: str = Field(..., description="URL-friendly slug for the cafe.")
    health_score: float = Field(..., description="Score of the cafe.")
    model_config = ConfigDict(json_schema_extra={
        "exemple": {
            "slug": "tore-et-fraction",
            "health_score": 5
        }
    })

class CafeUpdate(BaseModel):
    health_score: Optional[float] = Field(None, description="Score of the cafe.")
    public_recommendations: Optional[List[str]] = Field(None, description="List of recommended items in this cafe.")
    model_config = ConfigDict(json_schema_extra={
        "exemple": {
            "health_score": 5,
            "public_recommendations": [
                "cheeseburger",
            ]
        }
    })

class CafeHealthScoreUpdate(BaseModel):
    health_score: Optional[float] = Field(None, description="Score of the cafe.")
    model_config = ConfigDict(json_schema_extra={
        "exemple": {
            "health_score": 5
        }
    })

# ----------------------------------------------
#               User
# ----------------------------------------------

class PersonnalRecommendationOut(BaseModel):
    cafe_slug: str = Field(..., description="Slug of the cafe.")
    recommendation: List[str] = Field(..., description="List of slugs of recommended items in this cafe.")
    model_config = ConfigDict(json_schema_extra={
        "exemple": {
            "cafe_slug": "tore-et-fraction",
            "recommendation": [
                "cheeseburger",
            ]
        }
    })

class UserRecommendationOut(BaseModel):
    user_id: UUID = Field(..., description="ID of the user.")
    username: str = Field(..., description="Username of the user.")
    personnal_recommendations: List[PersonnalRecommendationOut] = Field(..., description="List of recommended items for the user.")
    cafe_recommendations: List[str] = Field(..., description="List of recommended cafes for the user.")
    model_config = ConfigDict(json_schema_extra={
        "exemple": {
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "username": "johndoe",
            "personnal_recommendations": [
                {
                    "cafe_slug": "tore-et-fraction",
                    "recommendation": [
                        "cheeseburger",
                    ]
                },
            ],
            "cafe_recommendations": [
                "tore-et-fraction"
            ]
        }
    })

class UserRecommendationUpdate(BaseModel):
    username: Optional[str] = Field(None, description="Username of the user.")
    personnal_recommendations: Optional[List[PersonnalRecommendationOut]] = Field(None, description="List of recommended items for the user.")
    cafe_recommendations: Optional[List[str]] = Field(None, description="List of recommended cafes for the user.")
    model_config = ConfigDict(json_schema_extra={
        "exemple": {
            "username": "johndoe",
            "personnal_recommendations": [
                {
                    "cafe_slug": "tore-et-fraction",
                    "recommendation": [
                        "cheeseburger",
                    ]
                },
            ],
            "cafe_recommendations": [
                "tore-et-fraction"
            ]
        }
    })