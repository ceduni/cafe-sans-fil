"""
Module for handling user-related routes.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status

from app.auth.dependencies import get_current_user
from app.auth.security import create_access_token
from app.config import settings
from app.user.models import (
    PasswordReset,
    PasswordResetRequest,
    User,
    UserAuth,
    UserOut,
    UserUpdate,
)
from app.user.service import UserService

user_router = APIRouter()


@user_router.get(
    "/users",
    response_model=List[UserOut],
)
async def get_users(
    request: Request,
    sort_by: str = Query("last_name", description="The field to sort the results by."),
    page: int = Query(1, description="The page number."),
    limit: int = Query(20, description="The number of users per page."),
    current_user: User = Depends(get_current_user),
) -> List[UserOut]:
    """Get a list of users (`member`)."""
    filters = dict(request.query_params)
    return await UserService.get_users(**filters)


@user_router.post(
    "/users",
    response_model=UserOut,
)
async def create_user(user: UserAuth) -> UserOut:
    """Create a user."""
    existing_attribute = await UserService.check_existing_user_attributes(
        user.email, user.matricule, user.username
    )
    if existing_attribute:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with this {existing_attribute} already exists",
        )

    created_user = await UserService.create_user(user)

    # Disable email sending because of Render blocking SMTP requests
    # # Don't send email to test domains
    # if await is_test_email(user.email):
    #     return created_user

    # email_context = {
    #     "title": "Bienvenue à Café sans-fil",
    #     "name": f"{user.first_name + ' ' + user.last_name}",
    # }
    # await send_registration_mail("Bienvenue à Café sans-fil", user.email, email_context)

    return created_user


@user_router.get(
    "/users/{username}",
    response_model=UserOut,
)
async def get_user(
    username: str = Path(..., description="The username of the user")
) -> UserOut:
    """Get a user. (`member`)"""
    user = await UserService.get_user_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@user_router.put(
    "/users/{username}",
    response_model=UserOut,
    description="Update a user. (`member`)",
)
async def update_user(
    user_data: UserUpdate,
    username: str = Path(..., description="The username of the user to update"),
    current_user: User = Depends(get_current_user),
) -> UserOut:
    """Update the details of an existing user."""
    user = await UserService.get_user_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Authorization check
    if username != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden"
        )

    return await UserService.update_user(username, user_data)


@user_router.delete(
    "/users/{username}",
    response_description="Delete User",
)
async def delete_user(
    username: str = Path(..., description="The username of the user to delete"),
    current_user: User = Depends(get_current_user),
):
    """Delete a user. (`member`)"""
    # Authorization check
    if current_user.username != username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden"
        )

    user = await UserService.delete_user(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return {"msg": f"User {username} has been deleted."}


# --------------------------------------
#               Reset Password
# --------------------------------------


@user_router.post(
    "/request-reset-password",
)
async def request_reset_password(user_email: PasswordResetRequest):
    """Request a password reset for a user via their email address."""
    user = await UserService.get_user_by_email(user_email.email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found with the provided email address.",
        )

    token = create_access_token(user.id)
    base_url = settings.BASE_URL
    reset_link = f"{base_url}/reset-password?token={token}"

    # Disable email sending because of Render blocking SMTP requests
    # await send_reset_password_mail("Réinitialisation du mot de passe", user.email,
    #     {
    #         "title": "Réinitialisation du mot de passe",
    #         "name": user.first_name + " " + user.last_name,
    #         "reset_link": reset_link
    #     }
    # )
    return {
        "msg": "Email has been sent with instructions to reset your password. (Mail disabled for now)",
        "reset_link": reset_link,
    }


@user_router.put(
    "/reset-password",
)
async def reset_password(
    new_password: PasswordReset,
    token: str = Query(..., description="The token received for password reset"),
):
    """Reset the password for a user using the provided token."""
    user = await get_current_user(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    await UserService.reset_password(user, new_password.password)
    return {"msg": "Password has been reset successfully."}
