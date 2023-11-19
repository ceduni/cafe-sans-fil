from pydantic import field_validator, ConfigDict, BaseModel, EmailStr, Field
from uuid import UUID
from typing import Optional
import re

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
    email: EmailStr = Field(..., description="User's email address, used for login and communication.")
    matricule: str = Field(..., pattern="^[a-z]{2}\d{5}$", min_length=7, max_length=7, description="Unique matricule identifier, consisting of two lowercase letters followed by five digits.")
    username: str = Field(..., min_length=3, max_length=20, description="Username for the user's account, used for identification within the system.")
    password: str = Field(..., min_length=8, max_length=30, description="Password for the user's account, used for account security.")
    first_name: str = Field(..., min_length=2, max_length=30, pattern="^[a-zA-ZÀ-ÿ' -]+$", description="User's first name, allowing letters, spaces, hyphens, and apostrophes.")
    last_name: str = Field(..., min_length=2, max_length=30, pattern="^[a-zA-ZÀ-ÿ' -]+$", description="User's last name, allowing letters, spaces, hyphens, and apostrophes.")
    photo_url: Optional[str] = Field(None, min_length=10, max_length=255, description="URL of the user's profile photo.")
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "email": "john.doe@example.com",
            "matricule": "jd12345",
            "username": "johndoe",
            "password": "Password123",
            "first_name": "John",
            "last_name": "Doe",
            "photo_url": "https://i.pinimg.com/474x/1d/2e/c1/1d2ec1fc1287c71fafa25879b7cd387a.jpg"
        }
    })

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$"
        if not re.match(pattern, v):
            raise ValueError('Password must contain upper and lower case letters and digits.')
        return v
    
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, description="New email address to update.")
    matricule: Optional[str] = Field(None, pattern="^[a-z]{2}\d{5}$", min_length=7, max_length=7, description="New matricule to update.")
    username: Optional[str] = Field(None, min_length=3, max_length=20, description="New username to update.")
    password: Optional[str] = Field(None, min_length=8, max_length=30, description="New password to update.")
    first_name: Optional[str] = Field(None, min_length=2, max_length=30, pattern="^[a-zA-ZÀ-ÿ' -]+$", description="New first name to update.")
    last_name: Optional[str] = Field(None, min_length=2, max_length=30, pattern="^[a-zA-ZÀ-ÿ' -]+$", description="New last name to update.")
    photo_url: Optional[str] = Field(None, min_length=10, max_length=255, description="New URL for the user's profile photo.")
    is_active: Optional[bool] = Field(None, description="Flag to indicate whether the user's account is active or not.")
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "email": "john.doe@example.com",
            "matricule": "jd12345",
            "username": "johndoe",
            "password": "Password123",
            "first_name": "John",
            "last_name": "Doe",
            "photo_url": "https://i.pinimg.com/474x/1d/2e/c1/1d2ec1fc1287c71fafa25879b7cd387a.jpg",
            "is_active": True
        }
    })

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$"
        if not re.match(pattern, v):
            raise ValueError('Password must contain upper and lower case letters and digits.')
        return v

class UserOut(BaseModel):
    user_id: UUID = Field(..., description="Unique identifier of the user.")
    email: EmailStr = Field(..., description="User's email address.")
    matricule: str = Field(..., description="User's matricule identifier.")
    username: str = Field(..., description="Username of the user.")
    first_name: str = Field(..., description="First name of the user.")
    last_name: str = Field(..., description="Last name of the user.")
    photo_url: Optional[str] = Field(None, description="URL of the user's profile photo.")
    is_active: bool = Field(..., description="Indicates whether the user's account is active.")
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "email": "john.doe@example.com",
            "matricule": "jd12345",
            "username": "johndoe",
            "first_name": "John",
            "last_name": "Doe",
            "photo_url": "https://i.pinimg.com/474x/1d/2e/c1/1d2ec1fc1287c71fafa25879b7cd387a.jpg",
            "is_active": True
        }
    })
