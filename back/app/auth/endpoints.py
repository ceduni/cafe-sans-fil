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
from app.email.service import EmailService
from app.models import ErrorResponse
from app.user.models import UserCreate, UserOut
from app.user.service import UserService

auth_router = APIRouter()


@auth_router.post(
    "/auth/login",
    response_model=TokenSchema,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    },
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """Authenticate user and return access and refresh tokens."""
    user = None
    if "@" in form_data.username:
        user = await UserService.get_by_email(email=form_data.username)
    else:
        user = await UserService.get_by_username(username=form_data.username)

    # Check account status
    # if user and not user.is_verified:
    #     raise HTTPException(status_code=403, detail="Please verify your email first")
    if user and not user.is_active:
        raise HTTPException(status_code=403, detail="Account is inactive")

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

    # Reset when inactivity for users who are not locked out
    if (
        user
        and not user.lockout_until
        and user.last_login_attempt
        and (datetime.now(UTC).replace(tzinfo=None) - user.last_login_attempt)
        >= timedelta(minutes=5)
    ):
        user.login_attempts = 0

    # Reset when inactivity for users who are locked out
    if (
        user
        and user.lockout_until
        and (datetime.now(UTC).replace(tzinfo=None) - user.last_login_attempt)
        >= timedelta(days=1)
    ):
        user.login_attempts = 0
        user.lockout_until = None

    authenticated_user = await AuthService.authenticate(
        credential=form_data.username, password=form_data.password
    )

    if not authenticated_user:
        if user:
            user.login_attempts += 1
            user.last_login_attempt = datetime.now(UTC)
            user.lockout_until = LockoutConfig.calculate_lockout_duration(
                user.login_attempts, user.lockout_until
            )
            await user.save()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # Reset on successful login
    if user:
        user.login_attempts = 0
        user.lockout_until = None
        user.last_login_attempt = None
        await user.save()

    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
    }


@auth_router.post(
    "/auth/register",
    response_model=UserOut,
    responses={
        409: {"model": ErrorResponse},
    },
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

    created_user = await UserService.create(user)
    if not await EmailService.is_test_email(user.email):
        await EmailService.send_verification_email(
            user_email=user.email,
            verification_link=f"{settings.BASE_URL}/auth/verify?token={create_access_token(created_user.id)}"
        )

    return created_user


@auth_router.post(
    "/auth/forgot-password",
)
async def forgot_password(
    email: str,
):
    """Request a password reset for a user via their email address."""
    user = await UserService.get_by_email(email)
    if user is None:
        return

    if not await EmailService.is_test_email(user.email):
        await EmailService.send_password_reset(
            user_email=user.email,
            reset_link=f"{settings.BASE_URL}/reset-password?token={create_access_token(user.id)}",
        )


@auth_router.put(
    "/auth/reset-password",
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    },
)
async def reset_password(
    body: ResetPasswordCreate,
):
    """Reset the password for a user using the provided token."""
    user = await get_current_user(body.token)

    await AuthService.reset_password(user, body.password)
    return {"msg": "Password has been reset successfully."}


@auth_router.post("/auth/verify")
async def verify_email(token: str = Body(...)):
    """Verify user's email address."""
    user = await get_current_user(token)
    if not user.is_verified:
        user.is_verified = True
        await user.save()


@auth_router.post(
    "/auth/refresh",
    response_model=TokenSchema,
    responses={
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def refresh_token(refresh_token: str = Body(...)):
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
    user = await UserService.get_by_id(token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid token for user",
        )
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
    }
