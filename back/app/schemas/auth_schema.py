from beanie import PydanticObjectId
from pydantic import BaseModel, Field

"""
This module provides data schemas related to authentication tokens.
"""


class TokenSchema(BaseModel):
    access_token: str = Field(..., description="JWT access token for authentication.")
    refresh_token: str = Field(
        ..., description="JWT refresh token to obtain a new access token."
    )


class TokenPayload(BaseModel):
    sub: PydanticObjectId = Field(None, description="Subject of the token.")
    exp: int = Field(None, description="Expiration time of the token.")
