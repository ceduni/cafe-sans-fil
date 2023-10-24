from pydantic import BaseModel, EmailStr, Field
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

class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="user email")
    matricule: str = Field(..., min_length=5, max_length=50, description="matricule")
    username: str = Field(..., min_length=1, max_length=50, description="username")
    hashed_password: str = Field(..., min_length=5, max_length=50, description="hashed password")
    first_name: str = Field(..., min_length=1, max_length=50, description="first name")
    last_name: str = Field(..., min_length=1, max_length=50, description="last name")

    class Config:
        schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "matricule": "M123456",
                "username": "johndoe",
                "hashed_password": "dWJ1bnR1MTIz",
                "first_name": "John",
                "last_name": "Doe"
            }
        }

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    matricule: Optional[str] = None
    username: Optional[str] = None
    hashed_password: Optional[str] = None # This will be hashed before saving
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "matricule": "M123456",
                "username": "johndoe",
                "hashed_password": "dWJ1bnR1MTIz",
                "first_name": "John",
                "last_name": "Doe"
            }
        }

class UserOut(BaseModel):
    user_id: UUID
    email: EmailStr
    matricule: str
    username: str
    #hashed_password: We don't want to show hashed password
    first_name: str
    last_name: str

    class Config:
        schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "john.doe@example.com",
                "matricule": "M123456",
                "username": "johndoe",
                "first_name": "John",
                "last_name": "Doe"
            }
        }
