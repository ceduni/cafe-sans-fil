"""
Module for handling auth-related operations.
"""

from typing import Optional

from app.auth.security import get_password, verify_password
from app.user.models import User
from app.user.service import UserService


class AuthService:
    """Service class for Auth operations."""

    @staticmethod
    async def authenticate(credential: str, password: str) -> Optional[User]:
        """Authenticate a user."""
        if "@" in credential:
            user = await UserService.get_user_by_email(email=credential)
        else:
            user = await UserService.get_user_by_username(username=credential)

        if not user:
            return None
        if not verify_password(password=password, hashed_pass=user.hashed_password):
            return None

        return user

    @staticmethod
    async def reset_password(user: User, new_password: str):
        """Reset a user's password."""
        hashed_password = get_password(new_password)
        await user.update({"$set": {"hashed_password": hashed_password}})
        return user
