from pydantic import ConfigDict, BaseModel, EmailStr, Field
from uuid import UUID
from typing import Optional

"""
This module defines the Pydantic-based schemas for user operations in the Café application. 
These schemas are utilized for request and response validation, serialization, 
and documentation specific to user accounts and profiles.

Note: These models are for API data interchange related to users and not direct database models.
"""

# --------------------------------------
#               User
# --------------------------------------

class UserAuth(BaseModel):
    email: EmailStr = Field(..., description="user email")
    matricule: str = Field(..., min_length=5, max_length=50, description="matricule")
    username: str = Field(..., min_length=1, max_length=50, description="username")
    password: str = Field(..., min_length=5, max_length=50, description="password")
    first_name: str = Field(..., min_length=1, max_length=50, description="first name")
    last_name: str = Field(..., min_length=1, max_length=50, description="last name")
    photo_url: Optional[str] = Field(None, min_length=1, max_length=755, description="photo url")
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "email": "john.doe@example.com",
            "matricule": "JD12345",
            "username": "johndoe",
            "password": "password123",
            "first_name": "John",
            "last_name": "Doe",
            "photo_url": "https://i.pinimg.com/474x/1d/2e/c1/1d2ec1fc1287c71fafa25879b7cd387a.jpg"
        }
    })

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, description="user email")
    matricule: Optional[str] = Field(None, min_length=5, max_length=50, description="matricule")
    username: Optional[str] = Field(None, min_length=1, max_length=50, description="username")
    password: Optional[str] = Field(None, min_length=5, max_length=50, description="password")
    first_name: Optional[str] = Field(None, min_length=1, max_length=50, description="first name")
    last_name: Optional[str] = Field(None, min_length=1, max_length=50, description="last name")
    photo_url: Optional[str] = Field(None, min_length=1, max_length=755, description="photo url")
    active: Optional[bool] = Field(None, description="is disabled")
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "email": "john.doe@example.com",
            "matricule": "JD12345",
            "username": "johndoe",
            "password": "password123",
            "first_name": "John",
            "last_name": "Doe",
            "photo_url": "https://i.pinimg.com/474x/1d/2e/c1/1d2ec1fc1287c71fafa25879b7cd387a.jpg",
            "active": True
        }
    })

class UserOut(BaseModel):
    user_id: UUID
    email: EmailStr
    matricule: str
    username: str
    first_name: str
    last_name: str
    photo_url: Optional[str] = None
    active: bool
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "email": "john.doe@example.com",
            "matricule": "JD12345",
            "username": "johndoe",
            "first_name": "John",
            "last_name": "Doe",
            "photo_url": "https://i.pinimg.com/474x/1d/2e/c1/1d2ec1fc1287c71fafa25879b7cd387a.jpg",
            "active": True
        }
    })
