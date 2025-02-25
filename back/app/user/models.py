"""
Module for handling user-related models.
"""

import re
from datetime import datetime
from typing import Optional

import pymongo
from beanie import Document
from pydantic import BaseModel, EmailStr, Field, field_validator
from pymongo import IndexModel

from app.models import Id


class UserBase(BaseModel):
    """Base model for users."""

    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    matricule: str = Field(..., pattern=r"^\d{6,8}$", min_length=6, max_length=8)
    first_name: str = Field(
        ..., min_length=2, max_length=30, pattern=r"^[a-zA-ZÀ-ÿ' -]+$"
    )
    last_name: str = Field(
        ..., min_length=2, max_length=30, pattern=r"^[a-zA-ZÀ-ÿ' -]+$"
    )
    photo_url: Optional[str] = Field(None, min_length=10, max_length=755)


class User(Document, UserBase):
    """User document model."""

    hashed_password: str
    failed_login_attempts: int = Field(default=0)
    last_failed_login_attempt: Optional[datetime] = Field(default=None)
    lockout_until: Optional[datetime] = Field(default=None)
    is_active: bool = True

    @classmethod
    async def by_email(cls, email: str) -> "User":
        """Get user by email."""
        return await cls.find_one(cls.email == email)

    async def increment_failed_login_attempts(self):
        """Increment failed login attempts."""
        self.failed_login_attempts += 1
        await self.save()

    async def reset_failed_login_attempts(self):
        """Reset failed login attempts."""
        self.failed_login_attempts = 0
        self.lockout_until = None
        await self.save()

    async def set_lockout(self, lockout_time: datetime):
        """Set lockout time."""
        self.lockout_until = lockout_time
        await self.save()

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

    password: str = Field(..., min_length=8, max_length=30)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str):
        """Validate username."""
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
    # ...


class UserUpdate(BaseModel):
    """Model for updating users."""

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
    def validate_username(cls, v: str):
        """Validate username."""
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
    # ...


class UserOut(UserBase, Id):
    """Model for user output."""

    pass
