import re
from datetime import datetime
from typing import Optional

from beanie import Document, Indexed, PydanticObjectId
from pydantic import BaseModel, EmailStr, Field, field_validator


class User(Document):
    username: Indexed(str, unique=True)
    email: Indexed(EmailStr, unique=True)
    matricule: Indexed(str, unique=True)
    hashed_password: str
    first_name: Indexed(str)
    last_name: Indexed(str)
    photo_url: Optional[str] = None

    # Hidden from out
    failed_login_attempts: int = Field(default=0)
    last_failed_login_attempt: Optional[datetime] = Field(default=None)
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
