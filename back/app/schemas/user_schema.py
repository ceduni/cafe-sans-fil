from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
    matricule: str
    username: str
    hashed_password: str # This will be hashed before saving
    first_name: str
    last_name: str

    class Config:
        schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "matricule": "M123456",
                "username": "johndoe",
                "hashed_password": "dWJ1bnR1MTIz",
                "first_name": "John",
                "last_name": "Doe"
            }
        }
