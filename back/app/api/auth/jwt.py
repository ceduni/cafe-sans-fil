from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from app.services.user_service import UserService
from app.core.security import create_access_token, create_refresh_token
from app.schemas.auth_schema import TokenSchema
from app.schemas.user_schema import UserOut
from app.models.user_model import User
from app.api.deps.user_deps import get_current_user
from app.core.config import settings
from app.schemas.auth_schema import TokenPayload
from pydantic import ValidationError
from jose import jwt
from datetime import datetime, timedelta

"""
This module provides API routes for user authentication and token management.
"""

auth_router = APIRouter()


class LockoutConfig:
    INITIAL_LOCKOUT_THRESHOLD = 5  # Attempts required for initial lockout
    EXTRA_TRIES_AFTER_LOCKOUT = 5  # Additional tries after each lockout
    LOCKOUT_DURATIONS = [5, 15, 30, 60]  # Lockout durations in minutes

    @staticmethod
    def calculate_lockout_duration(attempts: int, locked_time) -> timedelta:
        if attempts < LockoutConfig.INITIAL_LOCKOUT_THRESHOLD and not locked_time:
            return None

        locked_time = datetime.utcnow()
        for i, duration in enumerate(LockoutConfig.LOCKOUT_DURATIONS):
            if (
                attempts
                == LockoutConfig.INITIAL_LOCKOUT_THRESHOLD
                + i * LockoutConfig.EXTRA_TRIES_AFTER_LOCKOUT
            ):
                return locked_time + timedelta(minutes=duration)

        if (
            attempts
            > LockoutConfig.INITIAL_LOCKOUT_THRESHOLD
            + len(LockoutConfig.LOCKOUT_DURATIONS)
            * LockoutConfig.EXTRA_TRIES_AFTER_LOCKOUT
        ):
            return locked_time + timedelta(minutes=LockoutConfig.LOCKOUT_DURATIONS[-1])
        return locked_time


@auth_router.post(
    "/auth/login",
    summary="Create access and refresh tokens for user",
    response_model=TokenSchema,
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = None
    if "@" in form_data.username:
        user = await UserService.get_user_by_email(email=form_data.username)
    else:
        user = await UserService.get_user_by_username(username=form_data.username)

    # Check if inactive account
    if user and not user.is_active:
        raise HTTPException(status_code=403, detail="Account is inactive.")

    # Check if user is currently locked out
    if user and user.lockout_until and user.lockout_until > datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account temporarily locked due to multiple failed login attempts.",
        )

    # Reset failed_login_attempts when inactivity for Users who are not locked out
    if (
        user
        and not user.lockout_until
        and user.last_failed_login_attempt
        and (datetime.utcnow() - user.last_failed_login_attempt) >= timedelta(minutes=5)
    ):
        user.failed_login_attempts = 0

    # Reset failed_login_attempts when inactivity for Users who are locked out
    if (
        user
        and user.lockout_until
        and (datetime.utcnow() - user.last_failed_login_attempt) >= timedelta(days=1)
    ):
        user.failed_login_attempts = 0
        user.lockout_until = None

    authenticated_user = await UserService.authenticate(
        credential=form_data.username, password=form_data.password
    )

    if not authenticated_user:
        if user:
            user.failed_login_attempts += 1
            user.last_failed_login_attempt = datetime.utcnow()
            user.lockout_until = LockoutConfig.calculate_lockout_duration(
                user.failed_login_attempts, user.lockout_until
            )
            await user.save()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # Reset failed login attempts on successful login
    if user:
        user.failed_login_attempts = 0
        user.lockout_until = None
        user.last_failed_login_attempt = None
        await user.save()

    return {
        "access_token": create_access_token(user.user_id),
        "refresh_token": create_refresh_token(user.user_id),
    }


@auth_router.post(
    "/auth/test-token",
    summary="🔵 Test if the access token is valid",
    response_model=UserOut,
)
async def test_token(user: User = Depends(get_current_user)):
    return user


@auth_router.post("/auth/refresh", summary="Refresh token", response_model=TokenSchema)
async def refresh_token(refresh_token: str = Body(...)):
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
        "access_token": create_access_token(user.user_id),
        "refresh_token": create_refresh_token(user.user_id),
    }
