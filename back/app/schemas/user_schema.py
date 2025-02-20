from pydantic import field_validator, BaseModel, EmailStr, Field
from beanie import PydanticObjectId
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
    username: str = Field(..., min_length=3, max_length=20, description="Username for the user's account, used for identification within the system.")
    email: EmailStr = Field(..., description="User's email address, used for login and communication.")
    matricule: str = Field(..., pattern="^\d{6,8}$", min_length=6, max_length=8, description="Unique matricule identifier")
    password: str = Field(..., min_length=8, max_length=30, description="Password for the user's account, used for account security.")
    first_name: str = Field(..., min_length=2, max_length=30, pattern="^[a-zA-ZÀ-ÿ' -]+$", description="User's first name, allowing letters, spaces, hyphens, and apostrophes.")
    last_name: str = Field(..., min_length=2, max_length=30, pattern="^[a-zA-ZÀ-ÿ' -]+$", description="User's last name, allowing letters, spaces, hyphens, and apostrophes.")
    photo_url: Optional[str] = Field(None, min_length=10, max_length=755, description="URL of the user's profile photo.")

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if v.startswith('-') or v.endswith('-'):
            raise ValueError('Username cannot begin or end with a hyphen')
        if '--' in v:
            raise ValueError('Username cannot contain consecutive hyphens')
        if not re.match(r'^[A-Za-z\d-]+$', v):
            raise ValueError('Username may only contain alphanumeric characters or single hyphens')

        return v
    
    # @field_validator('password')
    # @classmethod
    # def validate_password(cls, v):
    #     pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$"
    #     if not re.match(pattern, v):
    #         raise ValueError('Password must contain upper and lower case letters and digits.')
    #     return v
    

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=20, description="New username to update.")
    email: Optional[EmailStr] = Field(None, description="New email address to update.")
    matricule: Optional[str] = Field(None, pattern="^\d{6,8}$", min_length=6, max_length=8, description="New matricule to update.")
    password: Optional[str] = Field(None, min_length=8, max_length=30, description="New password to update.")
    first_name: Optional[str] = Field(None, min_length=2, max_length=30, pattern="^[a-zA-ZÀ-ÿ' -]+$", description="New first name to update.")
    last_name: Optional[str] = Field(None, min_length=2, max_length=30, pattern="^[a-zA-ZÀ-ÿ' -]+$", description="New last name to update.")
    photo_url: Optional[str] = Field(None, min_length=10, max_length=755, description="New URL for the user's profile photo.")

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if v.startswith('-') or v.endswith('-'):
            raise ValueError('Username cannot begin or end with a hyphen')
        if '--' in v:
            raise ValueError('Username cannot contain consecutive hyphens')
        if not re.match(r'^[A-Za-z\d-]+$', v):
            raise ValueError('Username may only contain alphanumeric characters or single hyphens')

        return v
    
    # @field_validator('password')
    # @classmethod
    # def validate_password(cls, v):
    #     pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$"
    #     if not re.match(pattern, v):
    #         raise ValueError('Password must contain upper and lower case letters and digits.')
    #     return v

class UserOut(BaseModel):
    id: PydanticObjectId = Field(..., description="Unique identifier of the user.")
    username: str = Field(..., description="Username of the user.")
    email: EmailStr = Field(..., description="User's email address.")
    matricule: str = Field(..., description="User's matricule identifier.")
    first_name: str = Field(..., description="First name of the user.")
    last_name: str = Field(..., description="Last name of the user.")
    photo_url: Optional[str] = Field(None, description="URL of the user's profile photo.")


# --------------------------------------
#              Reset Password
# --------------------------------------

class PasswordResetRequest(BaseModel):
    email: EmailStr = Field(..., description="User's email address, used for password reset.")

class PasswordReset(BaseModel):
    password: str = Field(..., min_length=8, max_length=30, description="New password for the user's account, used for account security.")

    # @field_validator('password')
    # @classmethod
    # def validate_password(cls, v):
    #     pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$"
    #     if not re.match(pattern, v):
    #         raise ValueError('Password must contain upper and lower case letters and digits.')
    #     return v
