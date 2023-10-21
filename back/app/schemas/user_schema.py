from pydantic import BaseModel, EmailStr

"""
This module defines the Pydantic-based schemas for user operations in the Café application. 
These schemas are utilized for request and response validation, serialization, 
and documentation specific to user accounts and profiles.

Note: These models are for API data interchange related to users and not direct database models.
"""

class User(BaseModel):
    email: EmailStr
    matricule: str
    username: str
    hashed_password: str # This will be hashed before saving
    first_name: str
    last_name: str

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
