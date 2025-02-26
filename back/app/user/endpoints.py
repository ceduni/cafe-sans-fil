"""
Module for handling user-related routes.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status
from fastapi_pagination.ext.beanie import paginate
from fastapi_pagination.links import Page

from app.auth.dependencies import get_current_user
from app.models import ErrorResponse
from app.service import parse_query_params
from app.user.models import User, UserOut, UserUpdate
from app.user.service import UserService

user_router = APIRouter()


@user_router.get(
    "/users",
    response_model=Page[UserOut],
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    },
)
async def get_users(
    request: Request,
    sort_by: Optional[str] = Query(None, description="Sort by a specific field"),
    current_user: User = Depends(get_current_user),
):
    """Get a list of users. (`member`)"""
    filters = parse_query_params(dict(request.query_params))
    users = await UserService.get_all(**filters)
    return await paginate(users)


@user_router.get(
    "/users/{username}",
    response_model=UserOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def get_user(username: str = Path(..., description="Username of the user")):
    """Get a user. (`member`)"""
    user = await UserService.get_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@user_router.put(
    "/users/{username}",
    response_model=UserOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
)
async def update_user(
    data: UserUpdate,
    username: str = Path(..., description="Username of the user"),
    current_user: User = Depends(get_current_user),
):
    """Update a user. (`member`)"""
    user = await UserService.get_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Authorization check
    if username != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden"
        )

    return await UserService.update(username, data)


@user_router.delete(
    "/users/{username}",
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def delete_user(
    username: str = Path(..., description="Username of the user"),
    current_user: User = Depends(get_current_user),
):
    """Delete a user. (`member`)"""
    # Authorization check
    if current_user.username != username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden"
        )

    user = await UserService.delete(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return {"msg": f"User {username} has been deleted."}
