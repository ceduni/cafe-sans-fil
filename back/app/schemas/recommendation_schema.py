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

class RecommendationOut(BaseModel):
    recommendations: List[Dict[str, str | List[str]]] = Field(..., description="Recommendations for each cafe.")
    model_config = ConfigDict(json_schema_extra={
        "exemple": {
            "recommendations":  ['cheeseburger', "Cheeseburger Spécial"]
        }
    })

class RecommendationUpdate(BaseModel):
    recommendations: Optional[List[Dict[str, str | List[str]]]] = Field(..., description="Recommendations for each cafe.")
    model_config = ConfigDict(json_encoders={
        "exemple": {
            "recommendations":  ["cheeseburger", "Cheeseburger Spécial"]
        }
    })