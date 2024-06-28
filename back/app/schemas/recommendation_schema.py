from pydantic import field_validator, ConfigDict, BaseModel, EmailStr, Field
from uuid import UUID
from typing import List, Dict, Optional

"""
This module defines the Pydantic-based schemas for user recommendations. 
These schemas are utilized for request and response validation, serialization, 
and documentation specific to user item recommendations.

Note: These models are for API data interchange related to users and not direct database models.
"""

# ----------------------------------------------
#               Recommendations
# ----------------------------------------------

class ItemRecommendationOut(BaseModel):
    recommendations: Dict[str, str | List[str]] = Field(..., description="Recommendations for each cafe.")
    model_config = ConfigDict(json_schema_extra={
        "exemple": {
            "recommendations":  ['cheeseburger', "Cheeseburger Spécial"]
        }
    })

class ItemRecommendationUpdate(BaseModel):
    recommendations: Optional[Dict[str, str | List[str]]] = Field(..., description="Recommendations for each cafe.")
    model_config = ConfigDict(json_encoders={
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