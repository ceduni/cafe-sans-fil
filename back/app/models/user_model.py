from typing import Optional
from uuid import UUID, uuid4
from beanie import Document, Indexed
from pydantic import EmailStr, Field
from datetime import datetime

"""
This module defines the Pydantic-based models used in the Café application for user management, 
which are specifically designed for database interaction via the Beanie ODM 
(Object Document Mapper) for MongoDB. These models outline the structure, relationships, 
and constraints of the user-related data stored in the database.

Note: These models are intended for direct database interactions related to users and are 
different from the API data interchange models.
"""

class User(Document):
    user_id: UUID = Field(default_factory=uuid4)
    email: Indexed(EmailStr, unique=True)
    matricule: Indexed(str, unique=True)
    username: Indexed(str, unique=True)
    hashed_password: str
    first_name: Indexed(str)
    last_name: Indexed(str)
    photo_url: Optional[str] = None

    # Hidden from out
    failed_login_attempts: int = Field(default=0)
    last_failed_login_attempt:Optional[datetime] = Field(default=None)
    lockout_until: Optional[datetime] = Field(default=None)
    is_active: bool = True

    @classmethod
    async def by_email(self, email: str) -> "User":
        return await self.find_one(self.email == email)
    
    async def increment_failed_login_attempts(self):
        self.failed_login_attempts += 1
        await self.save()

    async def reset_failed_login_attempts(self):
        self.failed_login_attempts = 0
        self.lockout_until = None
        await self.save()

    async def set_lockout(self, lockout_time: datetime):
        self.lockout_until = lockout_time
        await self.save()

    class Settings:
        name = "users"
