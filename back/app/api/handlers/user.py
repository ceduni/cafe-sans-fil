from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user_schema import User
from app.services.user_service import UserService
from uuid import UUID

"""
This module defines the API routes related to user management in the application.
"""

user_router = APIRouter()

# --------------------------------------
#               User
# --------------------------------------

@user_router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: UUID):
    user = await UserService.retrieve_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.post("/users", response_model=User)
async def create_user(user: User):
    return await UserService.create_user(user)

@user_router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: UUID, user: User):
    return await UserService.update_user(user_id, user)
