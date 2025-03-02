"""
Module for handling user-related routes.
"""

from typing import Optional, TypeVar

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status
from fastapi_pagination import Params
from fastapi_pagination.customization import CustomizedPage, UseParams
from fastapi_pagination.ext.beanie import paginate
from fastapi_pagination.links import Page
from pymongo.errors import DuplicateKeyError

from app.auth.dependencies import get_current_user
from app.models import ErrorConflictResponse, ErrorResponse
from app.service import parse_query_params
from app.user.models import User, UserOut, UserUpdate
from app.user.service import UserService

T = TypeVar("T")


class UserParams(Params):
    """Custom pagination parameters."""

    size: int = Query(20, ge=1, le=100, description="Page size")
    page: int = Query(1, ge=1, description="Page number")
    sort_by: Optional[str] = Query(None, description="Sort by a specific field")


UserPage = CustomizedPage[
    Page[T],
    UseParams(UserParams),
]


user_router = APIRouter()


@user_router.get(
    "/users",
    response_model=UserPage[UserOut],
    responses={
        401: {"model": ErrorResponse},
    },
)
async def list_users(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    """Get a list of users. (`MEMBER`)"""
    filters = parse_query_params(dict(request.query_params))
    users = await UserService.get_all(to_list=False, **filters)
    return await paginate(users)


@user_router.get(
    "/users/me",
    response_model=UserOut,
    responses={
        401: {"model": ErrorResponse},
    },
)
async def get_current_user(
    current_user: User = Depends(get_current_user),
):
    """Get current user. (`MEMBER`)"""
    return current_user


@user_router.put(
    "/users/me",
    response_model=UserOut,
    responses={
        401: {"model": ErrorResponse},
        409: {"model": ErrorConflictResponse},
    },
)
async def update_current_user(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
):
    """Update current user. (`MEMBER`)"""
    try:
        return await UserService.update(current_user, data)
    except DuplicateKeyError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=[
                {
                    "msg": "User with these fields already exists.",
                    "fields": list(e.details.get("keyPattern", {}).keys()),
                }
            ],
        )


@user_router.get(
    "/users/{id}",
    response_model=UserOut,
    responses={
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def get_user(
    id: PydanticObjectId = Path(..., description="ID of the user"),
):
    """Get a user. (`MEMBER`)"""
    user = await UserService.get_by_id(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "User with this ID does not exist."}],
        )
    return user


@user_router.put(
    "/users/{id}",
    response_model=UserOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorConflictResponse},
    },
)
async def update_user(
    data: UserUpdate,
    id: PydanticObjectId = Path(..., description="ID of the user"),
    current_user: User = Depends(get_current_user),
):
    """Update a user. (`MEMBER`)"""
    user = await UserService.get_by_id(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "User with this ID does not exist."}],
        )

    if id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=[{"msg": "You can only update your own profile"}],
        )

    try:
        return await UserService.update(user, data)
    except DuplicateKeyError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=[
                {
                    "msg": "User with these fields already exists.",
                    "fields": list(e.details.get("keyPattern", {}).keys()),
                }
            ],
        )


@user_router.delete(
    "/users/{id}",
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def delete_user(
    id: PydanticObjectId = Path(..., description="ID of the user"),
    current_user: User = Depends(get_current_user),
):
    """Delete a user. (`MEMBER`)"""
    user = await UserService.get_by_id(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "User with this ID does not exist."}],
        )

    if id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=[{"msg": "You can only delete your own profile"}],
        )

    await UserService.delete(user)
