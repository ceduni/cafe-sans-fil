"""
Module for handling token-related models.
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
