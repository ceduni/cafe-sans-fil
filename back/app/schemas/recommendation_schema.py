from pydantic import ConfigDict, BaseModel, Field
from typing import List, Optional

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
    slug: str = Field(..., description="URL-friendly slug for the menu item.")
    health_score: int = Field(..., description="Health score of the item.")
    cluster: str = Field(..., description="String representing the cluster where the item belongs.")
    model_config = ConfigDict(json_schema_extra={
        "exemple": {
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
    bot_recommendations: List[ItemOut] = Field(..., description="List of recommended items in this cafe.")
    public_recommendations: List[ItemOut] = Field(..., description="List of recommended items in this cafe.")
    model_config = ConfigDict(json_schema_extra={
        "exemple": {
            "slug": "tore-et-fraction",
            "health_score": 5,
            "bot_recommendations": [
                {
                    "slug": "cheeseburger",
                    "health_score": 5,
                    "cluster": "0"
                },
            ],
            "public_recommendations": [
                {
                    "slug": "cheeseburger",
                    "health_score": 5,
                    "cluster": "0"
                },
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
    bot_recommendations: Optional[List[ItemOut]] = Field(..., description="List of recommended items in this cafe.")
    public_recommendations: Optional[List[ItemOut]] = Field(..., description="List of recommended items in this cafe.")
    model_config = ConfigDict(json_schema_extra={
        "exemple": {
            "health_score": 5,
            "bot_recommendations": [
                {
                    "slug": "cheeseburger",
                    "health_score": 5,
                    "cluster": "0"
                },
            ],
            "public_recommendations": [
                {
                    "slug": "cheeseburger",
                    "health_score": 5,
                    "cluster": "0"
                },
            ]
        }
    })
