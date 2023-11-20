from fastapi import APIRouter, HTTPException, Path, Query, status, Request, Depends
from app.schemas.user_schema import UserOut, UserUpdate, UserAuth, PasswordResetRequest, PasswordReset
from app.services.user_service import UserService
from uuid import UUID
from typing import List
from app.models.user_model import User
from app.api.deps.user_deps import get_current_user
from app.core.mail import send_registration_mail, send_reset_password_mail, is_test_email
from app.core.security import create_access_token
from app.core.config import settings

"""
This module defines the API routes related to user management in the application.
"""

user_router = APIRouter()

# --------------------------------------
#               User
# --------------------------------------

@user_router.get("/users", response_model=List[UserOut], summary="List Users", description="Retrieve a list of all users.")
async def list_users(request: Request, current_user: User = Depends(get_current_user)):
    filters = dict(request.query_params)
    return await UserService.list_users(**filters)

@user_router.get("/users/{user_id}", response_model=UserOut, summary="Get User", description="Retrieve detailed information about a specific user.")
async def get_user(user_id: UUID = Path(..., description="The unique identifier of the user"), current_user: User = Depends(get_current_user)):
    user = await UserService.retrieve_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@user_router.post("/users", response_model=UserOut, summary="Create User", description="Create a new user with the provided information.")
async def create_user(user: UserAuth):
    existing_attribute = await UserService.check_existing_user_attributes(user.email, user.matricule, user.username)
    if existing_attribute:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with this {existing_attribute} already exists"
        )

    created_user = await UserService.create_user(user)

    # Don't send email to test domains
    if await is_test_email(user.email):
        return created_user
    
    email_context = {
        "title": "Bienvenue à Café Sans-fil",
        "name": f"{user.first_name + ' ' + user.last_name}",
    }
    await send_registration_mail("Bienvenue à Café Sans-fil", user.email, email_context)

    return created_user

@user_router.put("/users/{user_id}", response_model=UserOut, summary="Update User", description="Update the details of an existing user.")
async def update_user(user_data: UserUpdate, user_id: UUID = Path(..., description="The unique identifier of the user to update"), current_user: User = Depends(get_current_user)):
    user = await UserService.retrieve_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Authorization check
    if user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden"
        )

    return await UserService.update_user(user_id, user_data)

# --------------------------------------
#               Reset Password
# --------------------------------------

@user_router.post("/request-reset-password", response_description="Password reset request", summary="Request Reset Password", description="Request a password reset for a user via their email address.")
async def request_reset_password(user_email: PasswordResetRequest):
    user = await UserService.get_user_by_email(user_email.email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found with the provided email address."
        )

    token = create_access_token(user.user_id)
    base_url = settings.BASE_URL
    reset_link = f"{base_url}/reset-password?token={token}"

    await send_reset_password_mail("Réinitialisation du mot de passe", user.email,
        {
            "title": "Réinitialisation du mot de passe",
            "name": user.first_name + " " + user.last_name,
            "reset_link": reset_link
        }
    )
    return {"msg": "Email has been sent with instructions to reset your password."}


@user_router.put("/reset-password", response_description="Password reset", summary="Reset Password", description="Reset the password for a user using the provided token.")
async def reset_password(new_password: PasswordReset, token: str = Query(..., description="The token received for password reset")):
    user = await get_current_user(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    await UserService.reset_password(user, new_password.password)
    return {"msg": "Password has been reset successfully."}