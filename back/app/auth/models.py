"""
Module for handling authentication-related models.
"""

from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class TokenSchema(BaseModel):
    """Model for token schema."""

    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    """Model for token payload."""

    sub: PydanticObjectId
    exp: int


class ResetPasswordCreate(BaseModel):
    """Model for password resets."""

    password: str = Field(..., min_length=8, max_length=30)
    token: str

    # @field_validator('password')
    # @classmethod
    # def validate_password(cls, v):
    #     pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$"
    #     if not re.match(pattern, v):
    #         raise ValueError('Password must contain upper and lower case letters and digits.')
    #     return v
