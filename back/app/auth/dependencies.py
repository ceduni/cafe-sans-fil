"""
Module for handling authentication-related dependencies.
"""

from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError

from app.auth.models import TokenPayload
from app.config import settings
from app.user.models import User
from app.user.service import UserService

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login", scheme_name="JWT"
)


async def _base_current_user(
    aggregate: bool, token: str = Depends(reuseable_oauth)
) -> User:
    """Base function for user authentication"""
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=[{"msg": "Token expired"}],
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=[{"msg": "Could not validate credentials"}],
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await UserService.get_by_id(
        id=token_data.sub,
        aggregate=aggregate,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "Could not find user."}],
        )

    return user


async def get_current_user(token: str = Depends(reuseable_oauth)) -> User:
    """Standard user dependency"""
    return await _base_current_user(aggregate=False, token=token)


async def get_current_user_aggregate(token: str = Depends(reuseable_oauth)) -> User:
    """User aggregate dependency"""
    return await _base_current_user(aggregate=True, token=token)
