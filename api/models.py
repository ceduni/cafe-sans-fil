from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import List

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    udem_email: EmailStr = Field(..., unique=True)
    first_name: str = Field(...)
    last_name: str = Field(...)
    roles: List[dict] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "3d2e3d2e3d2e3d2e3d2e3d2e",
                "udem_email": "john.doe@umontreal.ca",
                "first_name": "John",
                "last_name": "Doe",
                "roles": {
                    "cafe_id": "5f897f7d7d6d6d6d6d6d6d6d",
                    "role_type": "benevole"
                }
            }
        }