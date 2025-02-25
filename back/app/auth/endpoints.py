"""
Module for handling authentication-related routes.
"""

from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import ValidationError

from app.auth.dependencies import get_current_user
from app.auth.lockout import LockoutConfig
from app.auth.models import ResetPasswordCreate, TokenPayload, TokenSchema
from app.auth.security import create_access_token, create_refresh_token
from app.auth.service import AuthService
from app.config import settings
from app.user.models import User, UserCreate, UserOut
from app.user.service import UserService

auth_router = APIRouter()


@auth_router.post(
    "/auth/login",
    response_model=TokenSchema,
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """Authenticate user and return access and refresh tokens."""
    user = None
    if "@" in form_data.username:
        user = await UserService.get_user_by_email(email=form_data.username)
    else:
        user = await UserService.get_user_by_username(username=form_data.username)

    # Check if inactive account
    if user and not user.is_active:
        raise HTTPException(status_code=403, detail="Account is inactive.")

    # Check if user is currently locked out
    if (
        user
        and user.lockout_until
        and user.lockout_until > datetime.now(UTC).replace(tzinfo=None)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account temporarily locked due to multiple failed login attempts.",
        )

    # Reset whenu inactivity for users who are not locked out
    if (
        user
        and not user.lockout_until
        and user.last_failed_login_attempt
        and (datetime.now(UTC).replace(tzinfo=None) - user.last_failed_login_attempt)
        >= timedelta(minutes=5)
    ):
        user.failed_login_attempts = 0

    # Reset when inactivity for users who are locked out
    if (
        user
        and user.lockout_until
        and (datetime.now(UTC).replace(tzinfo=None) - user.last_failed_login_attempt)
        >= timedelta(days=1)
    ):
        user.failed_login_attempts = 0
        user.lockout_until = None

    authenticated_user = await AuthService.authenticate(
        credential=form_data.username, password=form_data.password
    )

    if not authenticated_user:
        if user:
            user.failed_login_attempts += 1
            user.last_failed_login_attempt = datetime.now(UTC)
            user.lockout_until = LockoutConfig.calculate_lockout_duration(
                user.failed_login_attempts, user.lockout_until
            )
            await user.save()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # Reset on successful login
    if user:
        user.failed_login_attempts = 0
        user.lockout_until = None
        user.last_failed_login_attempt = None
        await user.save()

    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
    }


@auth_router.post(
    "/auth/register",
    response_model=UserOut,
)
async def register(user: UserCreate) -> UserOut:
    """Register a new user."""
    existing_attribute = await UserService.check_existing_user_attributes(
        user.email, user.matricule, user.username
    )
    if existing_attribute:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with this {existing_attribute} already exists",
        )

    created_user = await UserService.create_user(user)

    # TODO: Render blocking SMTP requests
    # # Don't send email to test domains
    # if await is_test_email(user.email):
    #     return created_user

    # email_context = {
    #     "title": "Bienvenue à Café sans-fil",
    #     "name": f"{user.first_name + ' ' + user.last_name}",
    # }
    # await send_registration_mail("Bienvenue à Café sans-fil", user.email, email_context)

    return created_user


# --------------------------------------
#               Reset Password
# --------------------------------------


@auth_router.post(
    "/auth/forgot-password",
)
async def forgot_password(
    email: str,
):
    """Request a password reset for a user via their email address."""
    user = await UserService.get_user_by_email(email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found with the provided email address.",
        )

    token = create_access_token(user.id)
    reset_link = f"{settings.BASE_URL}/reset-password?token={token}"

    # TODO: Render blocking SMTP requests
    # await send_reset_password_mail("Réinitialisation du mot de passe", user.email,
    #     {
    #         "title": "Réinitialisation du mot de passe",
    #         "name": user.first_name + " " + user.last_name,
    #         "reset_link": reset_link
    #     }
    # )

    return {
        "reset_link": reset_link,
    }


@auth_router.put(
    "/auth/reset-password",
)
async def reset_password(
    body: ResetPasswordCreate,
):
    """Reset the password for a user using the provided token."""
    user = await get_current_user(body.token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    await AuthService.reset_password(user, body.password)
    return {"msg": "Password has been reset successfully."}


# --------------------------------------
#               Tokens
# --------------------------------------


@auth_router.post("/auth/refresh", response_model=TokenSchema)
async def refresh_token(refresh_token: str = Body(...)) -> TokenSchema:
    """Refresh access token using refresh token."""
    try:
        payload = jwt.decode(
            refresh_token,
            settings.JWT_REFRESH_SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await UserService.get_user_by_id(token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid token for user",
        )
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
    }


@auth_router.post(
    "/auth/test-token",
    response_model=UserOut,
)
async def test_token(user: User = Depends(get_current_user)) -> UserOut:
    """Verify access token and return user details. (`member`)"""
    return user
