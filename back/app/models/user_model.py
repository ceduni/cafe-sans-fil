from uuid import UUID, uuid4
from beanie import Document, Indexed
from pydantic import EmailStr, Field

class User(Document):
    user_id: UUID = Field(default_factory=uuid4, unique=True)
    email: Indexed(EmailStr, unique=True)
    matricule: Indexed(str, unique=True)
    username: Indexed(str, unique=True)
    hashed_password: str  # This will be hashed before saving
    first_name: str
    last_name: str

    class Collection:
        name = "users"
