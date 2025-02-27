"""
Module for handling user-related models.
"""

import re
from datetime import datetime
from typing import Optional

import pymongo
from pydantic import BaseModel, EmailStr, Field, field_validator
from pymongo import IndexModel

from app.models import CustomDocument, Id


class UserBase(BaseModel):
    """Base model for users."""

    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    matricule: str = Field(..., min_length=6, max_length=8, examples=["123456"])
    first_name: str = Field(..., min_length=2, max_length=30)
    last_name: str = Field(..., min_length=2, max_length=30)
    photo_url: Optional[str] = Field(None, min_length=10, max_length=755)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str):
        if v.startswith("-") or v.endswith("-"):
            raise ValueError("Username cannot begin or end with a hyphen")
        if "--" in v:
            raise ValueError("Username cannot contain consecutive hyphens")
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError(
                "Username can only contain letters, numbers, and underscores"
            )
        if not re.match(r"^[A-Za-z\d-]+$", v):
            raise ValueError(
                "Username may only contain alphanumeric characters or single hyphens"
            )
        return v

    @field_validator("matricule")
    @classmethod
    def validate_matricule(cls, v):
        if not re.match(r"^\d{6,8}$", v):
            raise ValueError("Matricule must contain exactly 6-8 digits")
        return v

    @field_validator("first_name")
    @classmethod
    def validate_first_name(cls, v):
        pattern = r"^[a-zA-ZÀ-ÿ' \-]+$"
        if not re.match(pattern, v):
            raise ValueError("First name contains invalid characters")
        return v

    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, v):
        pattern = r"^[a-zA-ZÀ-ÿ' \-]+$"
        if not re.match(pattern, v):
            raise ValueError("Last name contains invalid characters")
        return v


class User(CustomDocument, UserBase):
    """User document model."""

    hashed_password: str
    login_attempts: int = Field(default=0)
    last_login_attempt: Optional[datetime] = Field(default=None)
    lockout_until: Optional[datetime] = Field(default=None)
    is_active: bool = True

    class Settings:
        """Settings for user document."""

        name = "users"
        indexes = [
            IndexModel([("username", pymongo.ASCENDING)], unique=True),
            IndexModel([("email", pymongo.ASCENDING)], unique=True),
            IndexModel([("matricule", pymongo.ASCENDING)], unique=True),
            IndexModel([("first_name", pymongo.ASCENDING)]),
            IndexModel([("last_name", pymongo.ASCENDING)]),
        ]


class UserCreate(UserBase):
    """Model for creating users."""

    password: str = Field(..., min_length=6, max_length=100)

    # @field_validator('password')
    # ...


class UserUpdate(BaseModel):
    """Model for updating users."""

    username: Optional[str] = Field(None, min_length=3, max_length=20)
    email: Optional[EmailStr] = None
    matricule: Optional[str] = Field(
        None, min_length=6, max_length=8, examples=["123456"]
    )
    password: Optional[str] = Field(None, min_length=6, max_length=100)
    first_name: Optional[str] = Field(None, min_length=2, max_length=30)
    last_name: Optional[str] = Field(None, min_length=2, max_length=30)
    photo_url: Optional[str] = Field(None, min_length=10, max_length=755)

    # @field_validator('password')
    # ...


class UserOut(UserBase, Id):
    """Model for user output."""

    pass
