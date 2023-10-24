from uuid import UUID
from pydantic import BaseModel

"""
This module provides data schemas related to authentication tokens.
"""

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    
class TokenPayload(BaseModel):
    sub: UUID = None
    exp: int = None

class CustomOAuth2PasswordRequestForm(BaseModel):
    email: str
    password: str