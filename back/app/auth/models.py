from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: PydanticObjectId
    exp: int
