from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user_schema import UserOut, UserUpdate, UserAuth
from app.services.user_service import UserService
from uuid import UUID
from typing import List

"""
This module defines the API routes related to user management in the application.
"""

user_router = APIRouter()

# --------------------------------------
#               User
# --------------------------------------

@user_router.get("/users", response_model=List[UserOut])
async def list_users():
    return await UserService.list_users()

@user_router.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: UUID):
    user = await UserService.retrieve_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.post("/users", response_model=UserOut)
async def create_user(user: UserAuth):
    return await UserService.create_user(user)

@user_router.put("/users/{user_id}", response_model=UserOut)
async def update_user(user_id: UUID, user: UserUpdate):
    return await UserService.update_user(user_id, user)