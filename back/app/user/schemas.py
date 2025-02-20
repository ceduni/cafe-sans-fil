import re
from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, EmailStr, Field, field_validator

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
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    matricule: str = Field(..., pattern=r"^\d{6,8}$", min_length=6, max_length=8)
    password: str = Field(..., min_length=8, max_length=30)
    first_name: str = Field(
        ..., min_length=2, max_length=30, pattern=r"^[a-zA-ZÀ-ÿ' -]+$"
    )
    last_name: str = Field(
        ..., min_length=2, max_length=30, pattern=r"^[a-zA-ZÀ-ÿ' -]+$"
    )
    photo_url: Optional[str] = Field(None, min_length=10, max_length=755)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if v.startswith("-") or v.endswith("-"):
            raise ValueError("Username cannot begin or end with a hyphen")
        if "--" in v:
            raise ValueError("Username cannot contain consecutive hyphens")
        if not re.match(r"^[A-Za-z\d-]+$", v):
            raise ValueError(
                "Username may only contain alphanumeric characters or single hyphens"
            )

        return v

    # @field_validator('password')
    # @classmethod
    # def validate_password(cls, v):
    #     pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$"
    #     if not re.match(pattern, v):
    #         raise ValueError('Password must contain upper and lower case letters and digits.')
    #     return v


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=20)
    email: Optional[EmailStr] = None
    matricule: Optional[str] = Field(
        None, pattern=r"^\d{6,8}$", min_length=6, max_length=8
    )
    password: Optional[str] = Field(None, min_length=8, max_length=30)
    first_name: Optional[str] = Field(
        None, min_length=2, max_length=30, pattern=r"^[a-zA-ZÀ-ÿ' -]+$"
    )
    last_name: Optional[str] = Field(
        None, min_length=2, max_length=30, pattern=r"^[a-zA-ZÀ-ÿ' -]+$"
    )
    photo_url: Optional[str] = Field(None, min_length=10, max_length=755)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if v.startswith("-") or v.endswith("-"):
            raise ValueError("Username cannot begin or end with a hyphen")
        if "--" in v:
            raise ValueError("Username cannot contain consecutive hyphens")
        if not re.match(r"^[A-Za-z\d-]+$", v):
            raise ValueError(
                "Username may only contain alphanumeric characters or single hyphens"
            )

        return v

    # @field_validator('password')
    # @classmethod
    # def validate_password(cls, v):
    #     pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$"
    #     if not re.match(pattern, v):
    #         raise ValueError('Password must contain upper and lower case letters and digits.')
    #     return v


class UserOut(BaseModel):
    id: PydanticObjectId
    username: str
    email: EmailStr
    matricule: str
    first_name: str
    last_name: str
    photo_url: Optional[str] = None


# --------------------------------------
#              Reset Password
# --------------------------------------


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordReset(BaseModel):
    password: str = Field(..., min_length=8, max_length=30)

    # @field_validator('password')
    # @classmethod
    # def validate_password(cls, v):
    #     pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$"
    #     if not re.match(pattern, v):
    #         raise ValueError('Password must contain upper and lower case letters and digits.')
    #     return v
