from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user_schema import UserOut, UserUpdate, UserAuth
from app.services.user_service import UserService
from uuid import UUID
from typing import List
from app.models.user_model import User
from app.api.deps.user_deps import get_current_user

"""
This module defines the API routes related to user management in the application.
"""

user_router = APIRouter()

# --------------------------------------
#               User
# --------------------------------------

@user_router.get("/users", response_model=List[UserOut])
async def list_users(current_user: User = Depends(get_current_user)):
    return await UserService.list_users()

@user_router.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: UUID, current_user: User = Depends(get_current_user)):
    user = await UserService.retrieve_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.post("/users", response_model=UserOut)
async def create_user(user: UserAuth):
    return await UserService.create_user(user)

@user_router.put("/users/{user_id}", response_model=UserOut)
async def update_user(user_id: UUID, user: UserUpdate, current_user: User = Depends(get_current_user)):
    # Authorization check
    if user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    return await UserService.update_user(user_id, user)
